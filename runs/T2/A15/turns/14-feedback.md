$ cat > /tmp/patch2.py << 'PYEOF'
p = 'ngxtop/ngxtop.py'
s = open(p).read()

# --- SQLProcessor.__init__: add is_default_report flag ---
old = """class SQLProcessor(object):
    def __init__(self, report_queries, fields, index_fields=None):
        self.begin = False
        self.report_queries = report_queries
        self.index_fields = index_fields if index_fields is not None else []
"""
new = """class SQLProcessor(object):
    def __init__(self, report_queries, fields, index_fields=None, is_default_report=False):
        self.begin = False
        self.report_queries = report_queries
        self.index_fields = index_fields if index_fields is not None else []
        self.is_default_report = is_default_report
"""
assert old in s
s = s.replace(old, new, 1)

# --- Replace report() with results()-based implementation + structured report ---
old = """    def report(self):
        if not self.begin:
            return ''
        count = self.count()
        duration = time.time() - self.begin
        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
        output = [status % (duration, count, count / duration)]
        with closing(self.conn.cursor()) as cursor:
            for query in self.report_queries:
                if isinstance(query, tuple):
                    label, query = query
                else:
                    label = ''
                cursor.execute(query)
                columns = (d[0] for d in cursor.description)
                result = tabulate.tabulate(cursor.fetchall(), headers=columns, tablefmt='orgtbl', floatfmt='.3f')
                output.append('%s\\n%s' % (label, result))
        return '\\n\\n'.join(output)
"""
new = """    def status_line(self):
        \"\"\"Build the status line that prefixes the table report.\"\"\"
        count = self.count()
        duration = time.time() - self.begin
        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
        return status % (duration, count, count / duration)

    def results(self):
        \"\"\"Yield (label, columns, rows) for every report query.\"\"\"
        with closing(self.conn.cursor()) as cursor:
            for query in self.report_queries:
                if isinstance(query, tuple):
                    label, query = query
                else:
                    label = ''
                cursor.execute(query)
                columns = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                yield label, columns, rows

    def report(self):
        if not self.begin:
            return ''
        output = [self.status_line()]
        for label, columns, rows in self.results():
            result = tabulate.tabulate(rows, headers=columns, tablefmt='orgtbl', floatfmt='.3f')
            output.append('%s\\n%s' % (label, result))
        return '\\n\\n'.join(output)

    def json_report(self):
        \"\"\"Build the structured JSON representation of the default report.

        Returns a dict with exactly two keys: 'summary' (an object) and
        'detailed' (an array of objects).
        \"\"\"
        summary = {}
        detailed = []
        for idx, (label, columns, rows) in enumerate(self.results()):
            # The default report has exactly two queries: Summary then Detailed.
            if idx == 0:
                if rows:
                    summary = dict(zip(columns, rows[0]))
            else:
                for row in rows:
                    detailed.append(dict(zip(columns, row)))
        return {'summary': summary, 'detailed': detailed}
"""
assert old in s, "report() anchor missing"
s = s.replace(old, new, 1)

open(p,'w').write(s)
print("patched SQLProcessor")
PYEOF
.venv/bin/python /tmp/patch2.py && sed -n '447,510p' ngxtop/ngxtop.py
patched SQLProcessor

    def process(self, records):
        self.begin = time.time()
        insert = 'insert into log (%s) values (%s)' % (self.column_list, self.holder_list)
        logging.info('sqlite insert: %s', insert)
        with closing(self.conn.cursor()) as cursor:
            for r in records:
                cursor.execute(insert, r)

    def status_line(self):
        """Build the status line that prefixes the table report."""
        count = self.count()
        duration = time.time() - self.begin
        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
        return status % (duration, count, count / duration)

    def results(self):
        """Yield (label, columns, rows) for every report query."""
        with closing(self.conn.cursor()) as cursor:
            for query in self.report_queries:
                if isinstance(query, tuple):
                    label, query = query
                else:
                    label = ''
                cursor.execute(query)
                columns = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                yield label, columns, rows

    def report(self):
        if not self.begin:
            return ''
        output = [self.status_line()]
        for label, columns, rows in self.results():
            result = tabulate.tabulate(rows, headers=columns, tablefmt='orgtbl', floatfmt='.3f')
            output.append('%s\n%s' % (label, result))
        return '\n\n'.join(output)

    def json_report(self):
        """Build the structured JSON representation of the default report.

        Returns a dict with exactly two keys: 'summary' (an object) and
        'detailed' (an array of objects).
        """
        summary = {}
        detailed = []
        for idx, (label, columns, rows) in enumerate(self.results()):
            # The default report has exactly two queries: Summary then Detailed.
            if idx == 0:
                if rows:
                    summary = dict(zip(columns, rows[0]))
            else:
                for row in rows:
                    detailed.append(dict(zip(columns, row)))
        return {'summary': summary, 'detailed': detailed}

    def init_db(self):
        create_table = 'create table log (%s)' % self.column_list
        with closing(self.conn.cursor()) as cursor:
            logging.info('sqlite init: %s', create_table)
            cursor.execute(create_table)
            for idx, field in enumerate(self.index_fields):
                sql = 'create index log_idx%d on log (%s)' % (idx, field)
                logging.info('sqlite init: %s', sql)

[exit code: 0]