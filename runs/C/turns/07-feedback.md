$ sed -n '570,640p' ngxtop/ngxtop.py && echo "===utils===" && cat ngxtop/utils.py
        except curses.error:
            pass
        scr.refresh()

    signal.signal(signal.SIGALRM, print_report)
    signal.signal(signal.SIGHUP, _sighup_handler)  # Handle log rotation signals
    interval = float(arguments['--interval'])
    signal.setitimer(signal.ITIMER_REAL, 0.1, interval)


def process(arguments):
    access_log = arguments['--access-log']
    log_format = arguments['--log-format']
    if access_log is None and not sys.stdin.isatty():
        # assume logs can be fetched directly from stdin when piped
        access_log = 'stdin'
    if access_log is None:
        access_log, log_format = detect_log_config(arguments)

    logging.info('access_log: %s', access_log)
    logging.info('log_format: %s', log_format)
    if access_log != 'stdin' and not os.path.exists(access_log):
        error_exit('access log file "%s" does not exist' % access_log)

    if arguments['info']:
        print('nginx configuration file:\n ', detect_config_path())
        print('access log file:\n ', access_log)
        print('access log format:\n ', log_format)
        print('available variables:\n ', ', '.join(sorted(extract_variables(log_format))))
        return

    source = build_source(access_log, arguments)
    pattern = build_pattern(log_format)
    processor = build_processor(arguments)
    setup_reporter(processor, arguments)
    process_log(source, pattern, processor, arguments)


def main():
    args = docopt(__doc__, version='xstat 0.1')

    log_level = logging.WARNING
    if args['--verbose']:
        log_level = logging.INFO
    if args['--debug']:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
    logging.debug('arguments:\n%s', args)

    try:
        process(args)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
===utils===
import sys


def choose_one(choices, prompt):
    for idx, choice in enumerate(choices):
        print('%d. %s' % (idx + 1, choice))
    selected = None
    if sys.version[0] == '3':
        raw_input = input
    while not selected or selected <= 0 or selected > len(choices):
        selected = raw_input(prompt)
        try:
            selected = int(selected)
        except ValueError:
            selected = None
    return choices[selected - 1]


def error_exit(msg, status=1):
    sys.stderr.write('Error: %s\n' % msg)
    sys.exit(status)

[exit code: 0]