$ cd /repo 2>/dev/null; sed -n '85,140p' ngxtop/ngxtop.py; echo "---"; sed -n '465,480p' ngxtop/ngxtop.py


DEFAULT_QUERIES = [
    ('Summary:',
     '''SELECT
       count(1)                                    AS count,
       avg(bytes_sent)                             AS avg_bytes_sent,
       median(bytes_sent)                          AS median_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     ORDER BY %(--order-by)s DESC
     LIMIT %(--limit)s'''),

    ('Detailed:',
     '''SELECT
       %(--group-by)s,
       count(1)                                    AS count,
       avg(bytes_sent)                             AS avg_bytes_sent,
       median(bytes_sent)                          AS median_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     GROUP BY %(--group-by)s
     HAVING %(--having)s
     ORDER BY %(--order-by)s DESC
     LIMIT %(--limit)s''')
]

DEFAULT_FIELDS = set(['status_type', 'bytes_sent'])

# ======================
# sqlite custom aggregates
# ======================
class Median(object):
    """SQLite aggregate computing the median of a set of values.

    NULL values are ignored, matching the behaviour of the built-in avg().
    With an even number of values the two middle values are averaged.
    """

    def __init__(self):
        self.values = []

    def step(self, value):
        if value is None:
            return
        self.values.append(value)

    def finalize(self):
        if not self.values:
            return None
---
class SQLProcessor(object):
    def __init__(self, report_queries, fields, index_fields=None):
        self.begin = False
        self.report_queries = report_queries
        self.index_fields = index_fields if index_fields is not None else []
        self.column_list = ','.join(fields)
        self.holder_list = ','.join(':%s' % var for var in fields)
        self.conn = sqlite3.connect(':memory:')
        self.conn.create_aggregate('median', 1, Median)
        self.init_db()

    def process(self, records):
        self.begin = time.time()
        insert = 'insert into log (%s) values (%s)' % (self.column_list, self.holder_list)
        logging.info('sqlite insert: %s', insert)
        with closing(self.conn.cursor()) as cursor:

[exit code: 0]