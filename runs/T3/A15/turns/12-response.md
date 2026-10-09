Now I understand the codebase fully. The request asks to add median of `bytes_sent` next to the average. Following the existing naming convention (`avg_bytes_sent`), the median column should be named `median_bytes_sent` and appear in both `Summary:` and `Detailed:` reports, right after `avg_bytes_sent`.

SQLite has no built-in median. I'll need a workaround. A robust approach for arbitrary data is to compute the median via a correlated subquery / ORDER BY + LIMIT/OFFSET, or register a custom SQLite aggregate function `median` via Python's `create_aggregate`. The custom aggregate is the cleanest and works uniformly in both queries.

Let me implement:
1. Register a `median` aggregate function on the connection.
2. Add `median(bytes_sent) AS median_bytes_sent` to both DEFAULT_QUERIES, placed after `avg_bytes_sent`.

Let me check that median ignores NULL/0 and only counts actual bytes.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="READ">
<｜｜DSML｜｜ parameter name="path">ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
