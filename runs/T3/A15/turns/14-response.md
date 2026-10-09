The file is long. Instead of rewriting the whole file, I'll make targeted edits using a Python script to avoid errors.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">python3 - <<'EOF'
import re
p = "ngxtop/ngxtop.py"
s = open(p).read()

# 1. Add median column to both default queries right after avg_bytes_sent
old = "       avg(bytes_sent)                             AS avg_bytes_sent,\n"
new = ("       avg(bytes_sent)                             AS avg_bytes_sent,\n"
       "       median(bytes_sent)                          AS median_bytes_sent,\n")
count = s.count(old)
assert count == 2, count
s = s.replace(old, new)

# 2. Register median aggregate on the connection in SQLProcessor.__init__
old2 = "        self.conn = sqlite3.connect(':memory:')\n        self.init_db()\n"
new2 = ("        self.conn = sqlite3.connect(':memory:')\n"
        "        self.conn.create_aggregate('median', 1, _MedianAggregate)\n"
        "        self.init_db()\n")
assert s.count(old2) == 1
s = s.replace(old2, new2)

# 3. Insert _MedianAggregate class definition before the SQLProcessor class
marker = "# =================================\n# Records and statistic processor\n# =================================\n"
agg = '''class _MedianAggregate(object):
    """SQLite aggregate computing the median of a set of numeric values.

    NULL values are ignored, matching avg()'s behaviour.  The median is the
    conventional middle value: for an even count it is the mean of the two
    central values, so it stays consistent with avg() for small samples.
    """

    def __init__(self):
        self.values = []

    def step(self, value):
        if value is None:
            return
        try:
            self.values.append(float(value))
        except (TypeError, ValueError):
            pass

    def finalize(self):
        if not self.values:
            return None
        self.values.sort()
        n = len(self.values)
        mid = n // 2
        if n % 2 == 1:
            return self.values[mid]
        return (self.values[mid - 1] + self.values[mid]) / 2.0


'''
assert s.count(marker) == 1
s = s.replace(marker, agg + marker)

open(p, "w").write(s)
print("patched ok")
EOF</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
