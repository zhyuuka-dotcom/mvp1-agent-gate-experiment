$ ls -la ngxtop tests && echo "===README===" && head -100 README.rst
ngxtop:
total 44
drwxrwxr-x 2 z z  4096 Oct  8 23:03 .
drwxrwxr-x 6 z z  4096 Oct  7 05:15 ..
-rw-rw-r-- 1 z z     0 Oct  6 12:33 __init__.py
-rw-rw-r-- 1 z z  6032 Oct  8 23:03 config_parser.py
-rw-rw-r-- 1 z z 23519 Oct  6 12:33 ngxtop.py
-rw-rw-r-- 1 z z   548 Oct  6 12:33 utils.py

tests:
total 52
drwxrwxr-x 3 z    z    4096 Oct  6 12:34 .
drwxrwxr-x 6 z    z    4096 Oct  7 05:15 ..
drwxrwxr-x 2 z    z    4096 Oct  6 12:33 fixtures
-rw-rw-r-- 1 z    z    3183 Oct  6 12:33 test_caddy_integration.py
-rw-r--r-- 1 root root 1467 Oct  6 12:34 test_characterization.py
-rw-rw-r-- 1 z    z    3157 Oct  6 12:33 test_config_parser.py
-rw-rw-r-- 1 z    z    4218 Oct  6 12:33 test_debug_json_parsing.py
-rw-rw-r-- 1 z    z    2327 Oct  6 12:33 test_json_extraction_fix.py
-rw-rw-r-- 1 z    z    4664 Oct  6 12:33 test_log_rotation.py
-rw-rw-r-- 1 z    z    4551 Oct  6 12:33 test_parse_log.py
===README===
================================================================
``ngxtop`` - **real-time** metrics for nginx server (and others)
================================================================

**ngxtop** parses your nginx access log and outputs useful, ``top``-like, metrics of your nginx server.
So you can tell what is happening with your server in real-time.

    ``ngxtop`` is designed to run in a short-period time just like the ``top`` command for troubleshooting and monitoring
    your Nginx server at the moment. If you need a long running monitoring process or storing your webserver stats in external
    monitoring / graphing system, you can try `Luameter <https://luameter.com>`_.

``ngxtop`` tries to determine the correct location and format of nginx access log file by default, so you can just run
``ngxtop`` and having a close look at all requests coming to your nginx server. But it does not limit you to nginx
and the default top view. ``ngxtop`` is flexible enough for you to configure and change most of its behaviours.
You can query for different things, specify your log and format, even parse remote Apache common access log with ease.
See sample usages below for some ideas about what you can do with it.

Installation
------------

::

    pip install ngxtop


Note: ``ngxtop`` is primarily developed and tested with python2 but also supports python3.

Usage
-----

::

    Usage:
        ngxtop [options]
        ngxtop [options] (print|top|avg|sum) <var>
        ngxtop info

    Options:
        -l <file>, --access-log <file>  access log file to parse.
        -f <format>, --log-format <format>  log format as specify in log_format directive.
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
        
        Supported log formats: combined (default), common, caddy (for Caddy JSON access logs)

Samples
-------

Default output
~~~~~~~~~~~~~~

::

    $ ngxtop
    running for 411 seconds, 64332 records processed: 156.60 req/sec

    Summary:
    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |---------+------------------+-------+-------+-------+-------|
    |   64332 |         2775.251 | 61262 |  2994 |    71 |     5 |

    Detailed:
    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |------------------------------------------+---------+------------------+-------+-------+-------+-------|
    | /abc/xyz/xxxx                            |   20946 |          434.693 | 20935 |     0 |    11 |     0 |
    | /xxxxx.json                              |    5633 |         1483.723 |  5633 |     0 |     0 |     0 |
    | /xxxxx/xxx/xxxxxxxxxxxxx                 |    3629 |         6835.499 |  3626 |     0 |     3 |     0 |
    | /xxxxx/xxx/xxxxxxxx                      |    3627 |        15971.885 |  3623 |     0 |     4 |     0 |
    | /xxxxx/xxx/xxxxxxx                       |    3624 |         7830.236 |  3621 |     0 |     3 |     0 |
    | /static/js/minified/utils.min.js         |    3031 |         1781.155 |  2104 |   927 |     0 |     0 |
    | /static/js/minified/xxxxxxx.min.v1.js    |    2889 |         2210.235 |  2068 |   821 |     0 |     0 |
    | /static/tracking/js/xxxxxxxx.js          |    2594 |         1325.681 |  1927 |   667 |     0 |     0 |
    | /xxxxx/xxx.html                          |    2521 |          573.597 |  2520 |     0 |     1 |     0 |
    | /xxxxx/xxxx.json                         |    1840 |          800.542 |  1839 |     0 |     1 |     0 |

View top source IPs of clients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ ngxtop top remote_addr
    running for 20 seconds, 3215 records processed: 159.62 req/sec

[exit code: 0]