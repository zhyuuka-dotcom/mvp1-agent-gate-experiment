$ grep -n "def main\|error_exit\|print(\|print_table\|tabulate\|docopt\|status_line\|report\|running for" ngxtop/ngxtop.py | head -60
16:    -t <seconds>, --interval <seconds>  report interval when running in follow mode [default: 2.0]
21:    -n <number>, --limit <number>  limit the number of records included in report for top command [default: 10]
80:from docopt import docopt
81:import tabulate
84:from .utils import error_exit
435:    def __init__(self, report_queries, fields, index_fields=None):
437:        self.report_queries = report_queries
452:    def report(self):
457:        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
460:            for query in self.report_queries:
467:                result = tabulate.tabulate(cursor.fetchall(), headers=columns, tablefmt='orgtbl', floatfmt='.3f')
502:    print(processor.report())  # this will only run when start in --no-follow mode
511:        report_queries = [(label, query)]
514:        report_queries = []
518:            report_queries.append((label, query))
523:        report_queries = [(label, query)]
528:        report_queries = [(label, query)]
530:        report_queries = arguments['<query>']
533:        report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]
536:    for label, query in report_queries:
543:    processor = SQLProcessor(report_queries, processor_fields)
558:def setup_reporter(processor, arguments):
565:    def print_report(sig, frame):
566:        output = processor.report()
574:    signal.signal(signal.SIGALRM, print_report)
592:        error_exit('access log file "%s" does not exist' % access_log)
595:        print('nginx configuration file:\n ', detect_config_path())
596:        print('access log file:\n ', access_log)
597:        print('access log format:\n ', log_format)
598:        print('available variables:\n ', ', '.join(sorted(extract_variables(log_format))))
604:    setup_reporter(processor, arguments)
608:def main():
609:    args = docopt(__doc__, version='xstat 0.1')

[exit code: 0]