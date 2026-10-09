$ cd /repo 2>/dev/null; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/combined.log 2>&1 | grep -v Warning | grep -v "re\." | tail -12
running for 0 seconds, 2 records processed: 16194.22 req/sec

Summary:
|   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+---------------------+-------+-------+-------+-------|
|       2 |         2636.500 |            2636.500 |     1 |     0 |     1 |     0 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+---------------------+-------+-------+-------+-------|
| /api           |       1 |          153.000 |                 153 |     0 |     0 |     1 |     0 |
| /              |       1 |         5120.000 |                5120 |     1 |     0 |     0 |     0 |

[exit code: 0]