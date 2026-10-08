$ .venv/bin/python -m ngxtop.ngxtop -f main -c repro/nginx.conf --no-follow 2>/dev/null | head -20; echo "EXIT=${PIPESTATUS[0]}"
running for 0 seconds, 0 records processed: 0.00 req/sec

Summary:
|   count | avg_bytes_sent   |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       0 |                  |     0 |     0 |     0 |     0 |

Detailed:
| request_path   | count   | avg_bytes_sent   | 2xx   | 3xx   | 4xx   | 5xx   |
|----------------+---------+------------------+-------+-------+-------+-------|
EXIT=0

[exit code: 0]