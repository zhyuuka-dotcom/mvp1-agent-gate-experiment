$ cd /repo 2>/dev/null; grep -n "median\|Median\|create_aggregate" ngxtop/ngxtop.py
92:       median(bytes_sent)                          AS median_bytes_sent,
106:       median(bytes_sent)                          AS median_bytes_sent,
123:class Median(object):
124:    """SQLite aggregate computing the median of a set of values.
473:        self.conn.create_aggregate('median', 1, Median)

[exit code: 0]