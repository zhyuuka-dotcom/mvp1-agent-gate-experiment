$ sed -n '30,70p' README.rst

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

[exit code: 0]