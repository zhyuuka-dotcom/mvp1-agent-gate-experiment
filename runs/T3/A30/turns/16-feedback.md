$ cd /repo 2>/dev/null; python3 - <<'PYEOF'
import re
p='ngxtop/ngxtop.py'
s=open(p).read()

# 1. add median to both default queries
s=s.replace(
"""       avg(bytes_sent)                             AS avg_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     ORDER BY %(--order-by)s DESC""",
"""       avg(bytes_sent)                             AS avg_bytes_sent,
       median(bytes_sent)                          AS median_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     ORDER BY %(--order-by)s DESC""")

s=s.replace(
"""       avg(bytes_sent)                             AS avg_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     GROUP BY %(--group-by)s""",
"""       avg(bytes_sent)                             AS avg_bytes_sent,
       median(bytes_sent)                          AS median_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     GROUP BY %(--group-by)s""")

# 2. insert Median aggregate class after DEFAULT_FIELDS block
anchor = "DEFAULT_FIELDS = set(['status_type', 'bytes_sent'])\n"
median_cls = anchor + '''
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
        values = sorted(self.values)
        count = len(values)
        mid = count // 2
        if count % 2 == 1:
            return values[mid]
        return (values[mid - 1] + values[mid]) / 2.0

'''
assert anchor in s
s=s.replace(anchor, median_cls, 1)

# 3. register aggregate on connection
s=s.replace(
"        self.conn = sqlite3.connect(':memory:')\n",
"        self.conn = sqlite3.connect(':memory:')\n        self.conn.create_aggregate('median', 1, Median)\n", 1)

open(p,'w').write(s)
print("done")
PYEOF
done

[exit code: 0]