$ echo "=== ngxtop.py 11-12 ==="; sed -n '11,12p' ngxtop/ngxtop.py; echo "=== config_parser.py 78-90 ==="; sed -n '78,90p' ngxtop/config_parser.py; echo "=== ngxtop.py 580-588 ==="; sed -n '580,588p' ngxtop/ngxtop.py
=== ngxtop.py 11-12 ===
    -f <format>, --log-format <format>  log format as specify in log_format directive. [default: combined]
                                       Supported values: combined, common, caddy (for Caddy JSON format)
=== config_parser.py 78-90 ===
    Parse config for log_format directives
    :return: iterator over ('format name', 'format string') tuple of found directives
    """
    # log_format name [params]
    log_format = Literal('log_format') + parameter + Group(OneOrMore(parameter)) + semicolon
    log_format.ignore(pythonStyleComment)

    for directive in log_format.searchString(config).asList():
        name = directive[1]
        format_string = ''.join(directive[2])
        yield name, format_string


=== ngxtop.py 580-588 ===
def process(arguments):
    access_log = arguments['--access-log']
    log_format = arguments['--log-format']
    if access_log is None and not sys.stdin.isatty():
        # assume logs can be fetched directly from stdin when piped
        access_log = 'stdin'
    if access_log is None:
        access_log, log_format = detect_log_config(arguments)


[exit code: 0]