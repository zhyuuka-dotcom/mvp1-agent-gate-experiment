$ 
sed -n '504,560p' ngxtop/ngxtop.py | grep -n ""
1:
2:def build_processor(arguments):
3:    fields = arguments['<var>']
4:    if arguments['print']:
5:        label = ', '.join(fields) + ':'
6:        selections = ', '.join(fields)
7:        query = 'select %s from log group by %s' % (selections, selections)
8:        report_queries = [(label, query)]
9:    elif arguments['top']:
10:        limit = int(arguments['--limit'])
11:        report_queries = []
12:        for var in fields:
13:            label = 'top %s' % var
14:            query = 'select %s, count(1) as count from log group by %s order by count desc limit %d' % (var, var, limit)
15:            report_queries.append((label, query))
16:    elif arguments['avg']:
17:        label = 'average %s' % fields
18:        selections = ', '.join('avg(%s)' % var for var in fields)
19:        query = 'select %s from log' % selections
20:        report_queries = [(label, query)]
21:    elif arguments['sum']:
22:        label = 'sum %s' % fields
23:        selections = ', '.join('sum(%s)' % var for var in fields)
24:        query = 'select %s from log' % selections
25:        report_queries = [(label, query)]
26:    elif arguments['query']:
27:        report_queries = arguments['<query>']
28:        fields = arguments['<fields>']
29:    else:
30:        report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]
31:        fields = DEFAULT_FIELDS.union(set([arguments['--group-by']]))
32:
33:    for label, query in report_queries:
34:        logging.info('query for "%s":\n %s', label, query)
35:
36:    processor_fields = []
37:    for field in fields:
38:        processor_fields.extend(field.split(','))
39:
40:    processor = SQLProcessor(report_queries, processor_fields)
41:    return processor
42:
43:
44:def build_source(access_log, arguments):
45:    # constructing log source
46:    if access_log == 'stdin':
47:        lines = sys.stdin
48:    elif arguments['--no-follow']:
49:        lines = open(access_log)
50:    else:
51:        lines = follow(access_log)
52:    return lines
53:
54:
55:def setup_reporter(processor, arguments):
56:    if arguments['--no-follow']:
57:        return

[exit code: 0]