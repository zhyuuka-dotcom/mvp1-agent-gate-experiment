$ grep -n "report\|DEFAULT_QUERIES\|--group-by\|output-format\|def process\|def build_processor" ngxtop/ngxtop.py | head -40
16:    -t <seconds>, --interval <seconds>  report interval when running in follow mode [default: 2.0]
18:    -g <var>, --group-by <var>  group by variable [default: request_path]
21:    -n <number>, --limit <number>  limit the number of records included in report for top command [default: 10]
48:    $ ngxtop --group-by remote_addr
87:DEFAULT_QUERIES = [
102:       %(--group-by)s,
110:     GROUP BY %(--group-by)s
435:    def __init__(self, report_queries, fields, index_fields=None):
437:        self.report_queries = report_queries
444:    def process(self, records):
452:    def report(self):
460:            for query in self.report_queries:
490:def process_log(lines, pattern, processor, arguments):
502:    print(processor.report())  # this will only run when start in --no-follow mode
505:def build_processor(arguments):
511:        report_queries = [(label, query)]
514:        report_queries = []
518:            report_queries.append((label, query))
523:        report_queries = [(label, query)]
528:        report_queries = [(label, query)]
530:        report_queries = arguments['<query>']
533:        report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]
534:        fields = DEFAULT_FIELDS.union(set([arguments['--group-by']]))
536:    for label, query in report_queries:
543:    processor = SQLProcessor(report_queries, processor_fields)
558:def setup_reporter(processor, arguments):
565:    def print_report(sig, frame):
566:        output = processor.report()
574:    signal.signal(signal.SIGALRM, print_report)
580:def process(arguments):
604:    setup_reporter(processor, arguments)

[exit code: 0]