$ grep -n "format\|build_pattern\|extract_variables\|combined\|common" ngxtop/ngxtop.py | head -60
11:    -f <format>, --log-format <format>  log format as specify in log_format directive. [default: combined]
12:                                       Supported values: combined, common, caddy (for Caddy JSON format)
27:    --version  print version information.
30:    -c <file>, --config <file>  allow ngxtop to parse nginx config file for log format and location.
35:    All examples read nginx config file for access log location and format.
36:    If you want to specify the access log file and / or log format, use the -f and -a options.
56:    Analyze apache access log from remote machine using 'common' log format
57:    $ ssh remote tail -f /var/log/apache2/access.log | ngxtop -f common
83:from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern
302:    """Parse Caddy JSON log format and convert to ngxtop's expected format."""
306:            # Caddy logs have format: timestamp INFO http.log.access.log2 handled request {json}
415:    # Handle Caddy format separately
582:    log_format = arguments['--log-format']
587:        access_log, log_format = detect_log_config(arguments)
590:    logging.info('log_format: %s', log_format)
597:        print('access log format:\n ', log_format)
598:        print('available variables:\n ', ', '.join(sorted(extract_variables(log_format))))
602:    pattern = build_pattern(log_format)
616:    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

[exit code: 0]