$ .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g request_path 2>/dev/null
running for 0 seconds, 2 records processed: 12925.44 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       2 |         2636.500 |     1 |     0 |     1 |     0 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+-------+-------+-------+-------|
| /api           |       1 |          153.000 |     0 |     0 |     1 |     0 |
| /              |       1 |         5120.000 |     1 |     0 |     0 |     0 |

[exit code: 0]