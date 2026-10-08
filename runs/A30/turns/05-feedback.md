$ grep -n "format\|pattern\|build_pattern\|extract_variables\|pat\|log_format" ngxtop/ngxtop.py | head -60
11:    -f <format>, --log-format <format>  log format as specify in log_format directive. [default: combined]
12:                                       Supported values: combined, common, caddy (for Caddy JSON format)
18:    -g <var>, --group-by <var>  group by variable [default: request_path]
27:    --version  print version information.
30:    -c <file>, --config <file>  allow ngxtop to parse nginx config file for log format and location.
35:    All examples read nginx config file for access log location and format.
36:    If you want to specify the access log file and / or log format, use the -f and -a options.
41:    Top 10 requested path with status 404:
42:    $ ngxtop top request_path --filter 'status == 404'
53:    Average body bytes sent of 200 responses of requested path begin with 'foo':
54:    $ ngxtop avg bytes_sent --filter 'status == 200 and request_path.startswith("foo")'
56:    Analyze apache access log from remote machine using 'common' log format
83:from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern
178:def _should_reopen_file(file_path, current_inode, current_size):
184:        file_stat = os.stat(file_path)
204:def _open_file_with_retry(file_path, max_retries):
211:            file_stat = os.stat(file_path)
212:            f = open(file_path, 'r')
219:                logging.warning(f"Failed to open {file_path} (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s...")
222:                logging.error(f"Failed to open {file_path} after {max_retries} attempts: {e}")
279:def parse_request_path(record):
286:    return urlparse.urlparse(uri).path if uri else None
302:    """Parse Caddy JSON log format and convert to ngxtop's expected format."""
306:            # Caddy logs have format: timestamp INFO http.log.access.log2 handled request {json}
367:            record['request_path'] = urlparse.urlparse(uri).path if uri else None
414:def parse_log(lines, pattern):
415:    # Handle Caddy format separately
416:    if pattern == 'caddy':
420:    matches = (pattern.match(l) for l in lines)
427:    records = add_field('request_path', parse_request_path, records)
490:def process_log(lines, pattern, processor, arguments):
495:    records = parse_log(lines, pattern)
582:    log_format = arguments['--log-format']
587:        access_log, log_format = detect_log_config(arguments)
590:    logging.info('log_format: %s', log_format)
591:    if access_log != 'stdin' and not os.path.exists(access_log):
595:        print('nginx configuration file:\n ', detect_config_path())
597:        print('access log format:\n ', log_format)
598:        print('available variables:\n ', ', '.join(sorted(extract_variables(log_format))))
602:    pattern = build_pattern(log_format)
605:    process_log(source, pattern, processor, arguments)
616:    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

[exit code: 0]