$ 
sed -n '452,472p' ngxtop/ngxtop.py | grep -n ""; echo "==="; cat ngxtop/utils.py; echo "==="; sed -n '556,605p' ngxtop/ngxtop.py | grep -n ""
1:    def report(self):
2:        if not self.begin:
3:            return ''
4:        count = self.count()
5:        duration = time.time() - self.begin
6:        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
7:        output = [status % (duration, count, count / duration)]
8:        with closing(self.conn.cursor()) as cursor:
9:            for query in self.report_queries:
10:                if isinstance(query, tuple):
11:                    label, query = query
12:                else:
13:                    label = ''
14:                cursor.execute(query)
15:                columns = (d[0] for d in cursor.description)
16:                result = tabulate.tabulate(cursor.fetchall(), headers=columns, tablefmt='orgtbl', floatfmt='.3f')
17:                output.append('%s\n%s' % (label, result))
18:        return '\n\n'.join(output)
19:
20:    def init_db(self):
21:        create_table = 'create table log (%s)' % self.column_list
===
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
===
1:
2:
3:def setup_reporter(processor, arguments):
4:    if arguments['--no-follow']:
5:        return
6:
7:    scr = curses.initscr()
8:    atexit.register(curses.endwin)
9:
10:    def print_report(sig, frame):
11:        output = processor.report()
12:        scr.erase()
13:        try:
14:            scr.addstr(output)
15:        except curses.error:
16:            pass
17:        scr.refresh()
18:
19:    signal.signal(signal.SIGALRM, print_report)
20:    signal.signal(signal.SIGHUP, _sighup_handler)  # Handle log rotation signals
21:    interval = float(arguments['--interval'])
22:    signal.setitimer(signal.ITIMER_REAL, 0.1, interval)
23:
24:
25:def process(arguments):
26:    access_log = arguments['--access-log']
27:    log_format = arguments['--log-format']
28:    if access_log is None and not sys.stdin.isatty():
29:        # assume logs can be fetched directly from stdin when piped
30:        access_log = 'stdin'
31:    if access_log is None:
32:        access_log, log_format = detect_log_config(arguments)
33:
34:    logging.info('access_log: %s', access_log)
35:    logging.info('log_format: %s', log_format)
36:    if access_log != 'stdin' and not os.path.exists(access_log):
37:        error_exit('access log file "%s" does not exist' % access_log)
38:
39:    if arguments['info']:
40:        print('nginx configuration file:\n ', detect_config_path())
41:        print('access log file:\n ', access_log)
42:        print('access log format:\n ', log_format)
43:        print('available variables:\n ', ', '.join(sorted(extract_variables(log_format))))
44:        return
45:
46:    source = build_source(access_log, arguments)
47:    pattern = build_pattern(log_format)
48:    processor = build_processor(arguments)
49:    setup_reporter(processor, arguments)
50:    process_log(source, pattern, processor, arguments)

[exit code: 0]