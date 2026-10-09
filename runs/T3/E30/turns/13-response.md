Plan approved. Now implement. First, modify ngxtop/ngxtop.py:
1. Add a Median aggregate class.
2. Register it on the connection in init_db.
3. Add median(bytes_sent) AS median_bytes_sent to both DEFAULT_QUERIES.

Let me re-read the current DEFAULT_QUERIES and SQLProcessor to make exact edits. I already have them. I'll use targeted edits via python or rewrite. Since WRITE is full-overwrite, I'll read the whole file and produce a full rewrite. I already have the full content from the first read. Let me make the edits.

Key changes in ngxtop/ngxtop.py:
- After imports, add a `Median` class.
- In DEFAULT_QUERIES Summary: insert `median(bytes_sent) AS median_bytes_sent,` after avg line.
- Same for Detailed.
- In init_db: `self.conn.create_aggregate('median', 1, Median)`.

Let me write the new DEFAULT_QUERIES block. I'll do a full-file WRITE. I need exact current content — I have it from the first READ. Let me reconstruct carefully.

Actually safer: use sed/python to patch the file, but WRITE is the whitelisted tool; RUN isn't restricted though. RUN can edit files? The gate only restricts WRITE. But "写白名单外文件将被拒绝" applies to WRITE. Using RUN with sed could bypass but is risky/fragile. I'll use WRITE with full content.

Let me write the full file. I must reproduce it verbatim except changes. This is long but I have it. Let me do it.

Changes:
1. Insert Median class before `DEFAULT_QUERIES = [`.
2. Add median column in both queries.
3. Register aggregate in init_db.

Let me construct.Now implement. I'll add a `Median` aggregate class, register it, and add `median(bytes_sent) AS median_bytes_sent` to both queries.

WRITE ngxtop/ngxtop.py
<<<FILE_CONTENTS
"""ngxtop - ad-hoc query for nginx access log.

Usage:
    ngxtop [options]
    ngxtop [options] (print|top|avg|sum) <var> ...
    ngxtop info
    ngxtop [options] query <query> ...

Options:
    -l <file>, --access-log <file>  access log file to parse.
    -f <format>, --log-format <format>  log format as specify in log_format directive. [default: combined]
                                       Supported values: combined, common, caddy (for Caddy JSON format)
    --no-follow  ngxtop default behavior is to ignore current lines in log
                     and only watch for new lines as they are written to the access log.
                     Use this flag to tell ngxtop to process the current content of the access log instead.
    -t <seconds>, --interval <seconds>  report interval when running in follow mode [default: 2.0]

    -g <var>, --group-by <var>  group by variable [default: request_path]
    -w <var>, --having <expr>  having clause [default: 1]
    -o <var>, --order-by <var>  order of output for default query [default: count]
    -n <number>, --limit <number>  limit the number of records included in report for top command [default: 10]
    -a <exp> ..., --a <exp> ...  add exp (must be aggregation exp: sum, avg, min, max, etc.) into output

    -v, --verbose  more verbose output
    -d, --debug  print every line and parsed record
    -h, --help  print this help message.
    --version  print version information.

    Advanced / experimental options:
    -c <file>, --config <file>  allow ngxtop to parse nginx config file for log format and location.
    -i <filter-expression>, --filter <filter-expression>  filter in, records satisfied given expression are processed.
    -p <filter-expression>, --pre-filter <filter-expression> in-filter expression to check in pre-parsing phase.

Examples:
    All examples read nginx config file for access log location and format.
    If you want to specify the access log file and / or log format, use the -f and -a options.

    "top" like view of nginx requests
    $ ngxtop

    Top 10 requested path with status 404:
    $ ngxtop top request_path --filter 'status == 404'

    Top 10 requests with highest total bytes sent
    $ ngxtop --order-by 'avg(bytes_sent) * count'

    Top 10 remote address, e.g., who's hitting you the most
    $ ngxtop --group-by remote_addr

    Print requests with 4xx or 5xx status, together with status and http referer
    $ ngxtop -i 'status >= 400' print request status http_referer

    Average body bytes sent of 200 responses of requested path begin with 'foo':
    $ ngxtop avg bytes_sent --filter 'status == 200 and request_path.startswith("foo")'

    Analyze apache access log from remote machine using 'common' log format
    $ ssh remote tail -f /var/log/apache2/access.log | ngxtop -f common
    
    Analyze Caddy JSON access log:
    $ ngxtop -l /var/log/caddy/access.log -f caddy
"""
from __future__ import print_function
import atexit
from contextlib import closing
import curses
import json
import logging
import os
import sqlite3
import time
import sys
import signal
import stat

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from docopt import docopt
import tabulate

from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern
from .utils import error_exit


class Median(object):
    """SQLite aggregate function computing the median of a column of values.

    Registered as ``median()`` on the sqlite connection so that the default
    report can show the median of ``bytes_sent`` next to its average. NULL
    values (e.g. records without ``bytes_sent``) are ignored; when no value
    is passed at all the result is NULL.
    """

    def __init__(self):
        self.values = []

    def step(self, value):
        if value is not None:
            self.values.append(value)

    def finalize(self):
        if not self.values:
            return None
        values = sorted(self.values)
        n = len(values)
        mid = n // 2
        if n % 2 == 1:
            return values[mid]
        return (values[mid - 1] + values[mid]) / 2.0


DEFAULT_QUERIES = [
    ('Summary:',
     '''SELECT
       count(1)                                    AS count,
       avg(bytes_sent)                             AS avg_bytes_sent,
       median(bytes_sent)                          AS median_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     ORDER BY %(--order-by)s DESC
     LIMIT %(--limit)s'''),

    ('Detailed:',
     '''SELECT
       %(--group-by)s,
       count(1)                                    AS count,
       avg(bytes_sent)                             AS avg_bytes_sent,
       median(bytes_sent)                          AS median_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     GROUP BY %(--group-by)s
     HAVING %(--having)s
     ORDER BY %(--order-by)s DESC
     LIMIT %(--limit)s''')
]

DEFAULT_FIELDS = set(['status_type', 'bytes_sent'])

# Global flag for log rotation signal
_rotation_requested = False


# ======================
# generator utilities
# ======================
def follow(the_file):
    """
    Follow a given file and yield new lines when they are available, like `tail -f`.
    Handles log rotation by detecting inode changes and file size resets.
    """
    f = None
    current_inode = None
    current_size = 0
    retry_count = 0
    max_retries = 5
    
    try:
        while True:
            # Check if we need to (re)open the file
            if f is None or _should_reopen_file(the_file, current_inode, current_size) or _check_rotation_signal():
                if f is not None:
                    f.close()
                    if _check_rotation_signal():
                        logging.info(f"SIGHUP received, reopening {the_file}...")
                        _clear_
