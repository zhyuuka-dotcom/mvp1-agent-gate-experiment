$ .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null | grep -A3 "Summary:"
Summary:
|   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+---------------------+-------+-------+-------+-------|
|       2 |         2636.500 |            2636.500 |     1 |     0 |     1 |     0 |

[exit code: 0]