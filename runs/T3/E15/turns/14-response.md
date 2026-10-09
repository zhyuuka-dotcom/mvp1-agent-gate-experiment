The rejections: R2 requires coverage across ≥2 different files, and my quote lines were too long (>120 chars). Let me use shorter exact substrings and add a quote from another file. The quote must be an exact substring, trimmed ≤120 chars.

Line: `       avg(bytes_sent)                             AS avg_bytes_sent,` — let me count: it's long. Let me find shorter substrings. `avg(bytes_sent)` is short. Let me use `       avg(bytes_sent)                             AS avg_bytes_sent,` — count chars roughly 7+13+ spaces... too long. I'll use shorter exact lines from the file.

Good short exact lines:
- `DEFAULT_QUERIES = [` (ngxtop.py:87)
- `self.conn = sqlite3.connect(':memory:')` (ngxtop.py:397)

And a second file: README.rst has `    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |`. Let me get an exact short line from README.rst.

Let me get exact line numbers/content.

RUN grep -n "DEFAULT_QUERIES = \[" ngxtop/ngxtop.py && grep -n "self.conn = sqlite3.connect" ngxtop/ngxtop.py && grep -n "avg_bytes_sent" README.rst | head -1

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -n "DEFAULT_QUERIES = \[" ngxtop/ngxtop.py && grep -n "self.conn = sqlite3.connect" ngxtop/ngxtop.py && grep -n "avg_bytes_sent" README.rst | head -1 && echo "---" && sed -n '76p;81p' README.rst</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
