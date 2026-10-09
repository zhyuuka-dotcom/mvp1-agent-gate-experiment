I'll implement the changes now. Let me write the updated `ngxtop.py`.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path" string="true">ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents" string="true">"""ngxtop - ad-hoc query for nginx access log.

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
    --output-format <fmt>  output format for the default report: table or json [default: table]

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

    Machine readable JSON output of the default report:
    $ ngxtop -l access.log --no-follow --output-format json
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


DEFAULT_QUERIES = [
    ('Summary:',
     '''SELECT
       count(1)                                    AS count,
       avg(bytes_sent)                             AS avg_bytes_sent,
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

VALID_OUTPUT_FORMATS = ('table', 'json')

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
                        _clear_rotation_signal()
                    else:
                        logging.info(f"Detected log rotation for {the_file}, reopening...")
                
                # Try to open the file with retries
                f, current_inode, current_size = _open_file_with_retry(the_file, max_retries)
                if f is None:
                    logging.error(f"Failed to open {the_file} after {max_retries} retries")
                    break
                
                f.seek(0, 2)  # seek to eof
                retry_count = 0
            
            # Read new lines
            line = f.readline()
            if not line:
                time.sleep(0.1)  # sleep briefly before trying again
                continue
            
            # Update current size
            current_size = f.tell()
            yield line
            
    except KeyboardInterrupt:
        if f is not None:
            f.close()
        raise
    except Exception as e:
        logging.error(f"Error in follow(): {e}")
        if f is not None:
            f.close()
        raise


def _should_reopen_file(file_path, current_inode, current_size):
    """
    Check if file should be reopened due to rotation.
    Returns True if file has been rotated (inode changed or size decreased significantly).
    """
    try:
        file_stat = os.stat(file_path)
        new_inode = file_stat.st_ino
        new_size = file_stat.st_size
        
        # File has been rotated if:
        # 1. Inode changed (file was moved/renamed)
        # 2. File size decreased significantly (> 1000 bytes, indicating truncation/rotation)
        if current_inode is not None and new_inode != current_inode:
            return True
        
        if new_size < current_size - 1000:  # Allow for some buffer, but detect major size drops
            return True
            
        return False
        
    except (OSError, IOError):
        # File doesn't exist or can't be accessed - we should try to reopen
        return True


def _open_file_with_retry(file_path, max_retries):
    """
    Open file with retry logic, handling temporary file absence during rotation.
    Returns (file_handle, inode, size) or (None, None, 0) if failed.
    """
    for attempt in range(max_retries):
       
