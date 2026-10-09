$ grep -n "DEFAULT_QUERIES = \[" ngxtop/ngxtop.py && grep -n "self.conn = sqlite3.connect" ngxtop/ngxtop.py && grep -n "avg_bytes_sent" README.rst | head -1 && echo "---" && sed -n '76p;81p' README.rst
87:DEFAULT_QUERIES = [
441:        self.conn = sqlite3.connect(':memory:')
76:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
---
    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |

[exit code: 0]