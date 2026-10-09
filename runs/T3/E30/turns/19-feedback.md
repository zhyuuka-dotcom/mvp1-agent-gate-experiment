$ grep -n "Median\|median\|create_aggregate" ngxtop/ngxtop.py
86:class Median(object):
87:    '''SQLite aggregate computing the median, ignoring NULLs.'''
113:       median(bytes_sent)                          AS median_bytes_sent,
127:       median(bytes_sent)                          AS median_bytes_sent,
465:        self.conn.create_aggregate('median', 1, Median)

[exit code: 0]