$ cd /tmp/t2c30/repo && .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g remote_addr,status 2>/dev/null; echo "EXIT=$?"
running for 0 seconds, 2 records processed: 16131.94 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       2 |         2636.500 |     1 |     0 |     1 |     0 |

Detailed:
| remote_addr   |   status |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------------+----------+---------+------------------+-------+-------+-------+-------|
| 10.0.0.1      |      200 |       1 |         5120.000 |     1 |     0 |     0 |     0 |
| 10.0.0.2      |      404 |       1 |          153.000 |     0 |     0 |     1 |     0 |
EXIT=0

[exit code: 0]