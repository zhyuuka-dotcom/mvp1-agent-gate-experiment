$ 
sed -n '380,600p' ngxtop/ngxtop.py | grep -n "" 
1:                    logging.info("="*80)
2:                    logging.info(f"Detailed JSON parsing error: {e}")
3:                    logging.info(f"Error position: line {e.lineno}, column {e.colno} (char {e.pos})")
4:                    logging.info(f"Line length: {len(line)} characters")
5:                    logging.info(f"Line ends with newline: {line.endswith(chr(10))}")
6:                    logging.info(f"JSON start position: {json_start}")
7:                    logging.info(f"Extracted JSON length: {len(json_str)} characters")
8:                    
9:                    # Show the area around the error
10:                    if e.pos is not None and e.pos < len(json_str):
11:                        start = max(0, e.pos - 20)
12:                        end = min(len(json_str), e.pos + 20)
13:                        logging.info(f"JSON around error position: ...{json_str[start:end]}...")
14:                        logging.info(f"                            {' ' * (e.pos - start - 3)}^")
15:                    
16:                    # Output the complete line for analysis
17:                    logging.info(f"Complete line from beginning ({len(line)} chars):")
18:                    # Show first 100 chars to see the prefix, then ... then area around JSON start
19:                    if len(line) > 200:
20:                        prefix = line[:100]
21:                        json_area = line[max(0, json_start-20):json_start+80]
22:                        logging.info(f"{prefix}...{json_area}...")
23:                    else:
24:                        logging.info(line.rstrip())
25:                    
26:                    # Output the extracted JSON string
27:                    logging.info(f"Extracted JSON string ({len(json_str)} chars):")
28:                    logging.info(json_str)
29:                    logging.info("="*80)
30:            else:
31:                logging.warning(f"Error parsing log line: {e}")
32:            continue
33:
34:
35:def parse_log(lines, pattern):
36:    # Handle Caddy format separately
37:    if pattern == 'caddy':
38:        return parse_caddy_log(lines)
39:        
40:    # Regular nginx/apache log parsing
41:    matches = (pattern.match(l) for l in lines)
42:    records = (m.groupdict() for m in matches if m is not None)
43:    records = map_field('status', to_int, records)
44:    records = add_field('status_type', parse_status_type, records)
45:    records = add_field('bytes_sent', lambda r: r['body_bytes_sent'], records)
46:    records = map_field('bytes_sent', to_int, records)
47:    records = map_field('request_time', to_float, records)
48:    records = add_field('request_path', parse_request_path, records)
49:    return records
50:
51:
52:# =================================
53:# Records and statistic processor
54:# =================================
55:class SQLProcessor(object):
56:    def __init__(self, report_queries, fields, index_fields=None):
57:        self.begin = False
58:        self.report_queries = report_queries
59:        self.index_fields = index_fields if index_fields is not None else []
60:        self.column_list = ','.join(fields)
61:        self.holder_list = ','.join(':%s' % var for var in fields)
62:        self.conn = sqlite3.connect(':memory:')
63:        self.init_db()
64:
65:    def process(self, records):
66:        self.begin = time.time()
67:        insert = 'insert into log (%s) values (%s)' % (self.column_list, self.holder_list)
68:        logging.info('sqlite insert: %s', insert)
69:        with closing(self.conn.cursor()) as cursor:
70:            for r in records:
71:                cursor.execute(insert, r)
72:
73:    def report(self):
74:        if not self.begin:
75:            return ''
76:        count = self.count()
77:        duration = time.time() - self.begin
78:        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
79:        output = [status % (duration, count, count / duration)]
80:        with closing(self.conn.cursor()) as cursor:
81:            for query in self.report_queries:
82:                if isinstance(query, tuple):
83:                    label, query = query
84:                else:
85:                    label = ''
86:                cursor.execute(query)
87:                columns = (d[0] for d in cursor.description)
88:                result = tabulate.tabulate(cursor.fetchall(), headers=columns, tablefmt='orgtbl', floatfmt='.3f')
89:                output.append('%s\n%s' % (label, result))
90:        return '\n\n'.join(output)
91:
92:    def init_db(self):
93:        create_table = 'create table log (%s)' % self.column_list
94:        with closing(self.conn.cursor()) as cursor:
95:            logging.info('sqlite init: %s', create_table)
96:            cursor.execute(create_table)
97:            for idx, field in enumerate(self.index_fields):
98:                sql = 'create index log_idx%d on log (%s)' % (idx, field)
99:                logging.info('sqlite init: %s', sql)
100:                cursor.execute(sql)
101:
102:    def count(self):
103:        with closing(self.conn.cursor()) as cursor:
104:            cursor.execute('select count(1) from log')
105:            return cursor.fetchone()[0]
106:
107:
108:# ===============
109:# Log processing
110:# ===============
111:def process_log(lines, pattern, processor, arguments):
112:    pre_filer_exp = arguments['--pre-filter']
113:    if pre_filer_exp:
114:        lines = (line for line in lines if eval(pre_filer_exp, {}, dict(line=line)))
115:
116:    records = parse_log(lines, pattern)
117:
118:    filter_exp = arguments['--filter']
119:    if filter_exp:
120:        records = (r for r in records if eval(filter_exp, {}, r))
121:
122:    processor.process(records)
123:    print(processor.report())  # this will only run when start in --no-follow mode
124:
125:
126:def build_processor(arguments):
127:    fields = arguments['<var>']
128:    if arguments['print']:
129:        label = ', '.join(field
…[RUN 输出截断：全长 9609 字符]
R_REAL, 0.1, interval)
199:
200:
201:def process(arguments):
202:    access_log = arguments['--access-log']
203:    log_format = arguments['--log-format']
204:    if access_log is None and not sys.stdin.isatty():
205:        # assume logs can be fetched directly from stdin when piped
206:        access_log = 'stdin'
207:    if access_log is None:
208:        access_log, log_format = detect_log_config(arguments)
209:
210:    logging.info('access_log: %s', access_log)
211:    logging.info('log_format: %s', log_format)
212:    if access_log != 'stdin' and not os.path.exists(access_log):
213:        error_exit('access log file "%s" does not exist' % access_log)
214:
215:    if arguments['info']:
216:        print('nginx configuration file:\n ', detect_config_path())
217:        print('access log file:\n ', access_log)
218:        print('access log format:\n ', log_format)
219:        print('available variables:\n ', ', '.join(sorted(extract_variables(log_format))))
220:        return
221:

[exit code: 0]