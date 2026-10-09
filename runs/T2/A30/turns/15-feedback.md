$ FMT='$remote_addr - - [$time_local] "$request" $status $bytes_sent'
echo "=== table ==="; .venv/bin/python -m ngxtop.ngxtop -f "$FMT" -l repro/combined.log --no-follow -g remote_addr 2>/dev/null
echo "=== json ==="; .venv/bin/python -m ngxtop.ngxtop -f "$FMT" -l repro/combined.log --no-follow -g remote_addr --output-format json 2>/dev/null
=== table ===
running for 0 seconds, 0 records processed: 0.00 req/sec

Summary:
|   count | avg_bytes_sent   |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       0 |                  |     0 |     0 |     0 |     0 |

Detailed:
| remote_addr   | count   | avg_bytes_sent   | 2xx   | 3xx   | 4xx   | 5xx   |
|---------------+---------+------------------+-------+-------+-------+-------|
=== json ===
{"summary": {"count": 0, "avg_bytes_sent": null, "2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}, "detailed": []}

[exit code: 0]