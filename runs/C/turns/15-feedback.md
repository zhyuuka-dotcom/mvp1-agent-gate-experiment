$ sed -n '1,90p' ngxtop/ngxtop.py
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


DEFAULT_QUERIES = [
    ('Summary:',
     '''SELECT
       count(1)                                    AS count,

[exit code: 0]