$ 
cat -n ngxtop/ngxtop.py
     1	"""ngxtop - ad-hoc query for nginx access log.
     2	
     3	Usage:
     4	    ngxtop [options]
     5	    ngxtop [options] (print|top|avg|sum) <var> ...
     6	    ngxtop info
     7	    ngxtop [options] query <query> ...
     8	
     9	Options:
    10	    -l <file>, --access-log <file>  access log file to parse.
    11	    -f <format>, --log-format <format>  log format as specify in log_format directive. [default: combined]
    12	                                       Supported values: combined, common, caddy (for Caddy JSON format)
    13	    --no-follow  ngxtop default behavior is to ignore current lines in log
    14	                     and only watch for new lines as they are written to the access log.
    15	                     Use this flag to tell ngxtop to process the current content of the access log instead.
    16	    -t <seconds>, --interval <seconds>  report interval when running in follow mode [default: 2.0]
    17	
    18	    -g <var>, --group-by <var>  group by variable [default: request_path]
    19	    -w <var>, --having <expr>  having clause [default: 1]
    20	    -o <var>, --order-by <var>  order of output for default query [default: count]
    21	    -n <number>, --limit <number>  limit the number of records included in report for top command [default: 10]
    22	    -a <exp> ..., --a <exp> ...  add exp (must be aggregation exp: sum, avg, min, max, etc.) into output
    23	
    24	    -v, --verbose  more verbose output
    25	    -d, --debug  print every line and parsed record
    26	    -h, --help  print this help message.
    27	    --version  print version information.
    28	
    29	    Advanced / experimental options:
    30	    -c <file>, --config <file>  allow ngxtop to parse nginx config file for log format and location.
    31	    -i <filter-expression>, --filter <filter-expression>  filter in, records satisfied given expression are processed.
    32	    -p <filter-expression>, --pre-filter <filter-expression> in-filter expression to check in pre-parsing phase.
    33	
    34	Examples:
    35	    All examples read nginx config file for access log location and format.
    36	    If you want to specify the access log file and / or log format, use the -f and -a options.
    37	
    38	    "top" like view of nginx requests
    39	    $ ngxtop
    40	
    41	    Top 10 requested path with status 404:
    42	    $ ngxtop top request_path --filter 'status == 404'
    43	
    44	    Top 10 requests with highest total bytes sent
    45	    $ ngxtop --order-by 'avg(bytes_sent) * count'
    46	
    47	    Top 10 remote address, e.g., who's hitting you the most
    48	    $ ngxtop --group-by remote_addr
    49	
    50	    Print requests with 4xx or 5xx status, together with status and http referer
    51	    $ ngxtop -i 'status >= 400' print request status http_referer
    52	
    53	    Average body bytes sent of 200 responses of requested path begin with 'foo':
    54	    $ ngxtop avg bytes_sent --filter 'status == 200 and request_path.startswith("foo")'
    55	
    56	    Analyze apache access log from remote machine using 'common' log format
    57	    $ ssh remote tail -f /var/log/apache2/access.log | ngxtop -f common
    58	    
    59	    Analyze Caddy JSON access log:
    60	    $ ngxtop -l /var/log/caddy/access.log -f caddy
    61	"""
    62	from __future__ import print_function
    63	import atexit
    64	from contextlib import closing
    65	import curses
    66	import json
    67	import logging
    68	import os
    69	import sqlite3
    70	import time
    71	import sys
    72	import signal
    73	import stat
    74	
    75	try:
    76	    import urlparse
    77	except ImportError:
    78	    import urllib.parse as urlparse
    79	
    80	from docopt import docopt
    81	import tabulate
    82	
    83	from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern
    84	from .utils import error_exit
    85	
    86	
    87	DEFAULT_QUERIES = [
    88	    ('Summary:',
    89	     '''SELECT
    90	       count(1)                                    AS count,
    91	       avg(bytes_sent)                             AS avg_bytes_sent,
    92	       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
    93	       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
    94	       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
    95	       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
    96	     FROM log
    97	     ORDER BY %(--order-by)s DESC
    98	     LIMIT %(--limit)s'''),
    99	
   100	    ('Detailed:',
   101	     '''SELECT
   102	       %(--group-by)s,
   103	       count(1)                                    AS count,
   104	       avg(bytes_sent)                             AS avg_bytes_sent,
   105	       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
   106	       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
   107	       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
   108	       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
   109	     FROM log
   110	     GROUP BY %(--group-by)s
   111	     HAVING %(--having)s
   112	     ORDER BY %(--order-by)s DESC
   113	     LIMIT %(--limit)s''')
   114	]
   115	
   116	DEFAULT_FIELDS = set(['status_type', 'bytes_sent'])
   117	
   118	# Global flag for log rotation signal
   119	_rotation_requested = False
   120	
   121	
   122	# ======================
   123	# generator utilities
   124	# ======================
   125	def follow(the_file):
   126	    """
   127	    Follow a given file and yield new lines when they are available, like `tail -f`.
   128	    Handles log rotation by detecting inode changes and file size resets.
   129	    """
   130	    f = None
   131	    current_inode = None
   132	    current_size = 0
   133	    retry_count = 0
   134	    max_retries = 5
   135	    
   136	    try:
   137	        while True:
   138	            # Check if we need to (re)open the file
   139	            if f is Non
…[RUN 输出截断：全长 27901 字符]
format)
   598	        print('available variables:\n ', ', '.join(sorted(extract_variables(log_format))))
   599	        return
   600	
   601	    source = build_source(access_log, arguments)
   602	    pattern = build_pattern(log_format)
   603	    processor = build_processor(arguments)
   604	    setup_reporter(processor, arguments)
   605	    process_log(source, pattern, processor, arguments)
   606	
   607	
   608	def main():
   609	    args = docopt(__doc__, version='xstat 0.1')
   610	
   611	    log_level = logging.WARNING
   612	    if args['--verbose']:
   613	        log_level = logging.INFO
   614	    if args['--debug']:
   615	        log_level = logging.DEBUG
   616	    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
   617	    logging.debug('arguments:\n%s', args)
   618	
   619	    try:
   620	        process(args)
   621	    except KeyboardInterrupt:
   622	        sys.exit(0)
   623	
   624	
   625	if __name__ == '__main__':
   626	    main()

[exit code: 0]