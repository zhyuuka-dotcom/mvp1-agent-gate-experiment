$ sed -n '440,475p' ngxtop/ngxtop.py
        self.report_queries = report_queries
        self.index_fields = index_fields if index_fields is not None else []
        self.column_list = ','.join(fields)
        self.holder_list = ','.join(':%s' % var for var in fields)
        self.conn = sqlite3.connect(':memory:')
        self.init_db()

    def process(self, records):
        self.begin = time.time()
        insert = 'insert into log (%s) values (%s)' % (self.column_list, self.holder_list)
        logging.info('sqlite insert: %s', insert)
        with closing(self.conn.cursor()) as cursor:
            for r in records:
                cursor.execute(insert, r)

    def report(self):
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
                output.append('%s\n%s' % (label, result))
        return '\n\n'.join(output)

    def init_db(self):
        create_table = 'create table log (%s)' % self.column_list

[exit code: 0]