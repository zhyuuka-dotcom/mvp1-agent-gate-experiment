$ cd /repo 2>/dev/null; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/access.log -c repro/nginx.conf 2>&1 | grep -v SyntaxWarning | grep -v "re.findall\|re.split\|name = \|value = \|matched = " | head -40
running for 0 seconds, 0 records processed: 0.00 req/sec

Summary:
|   count | avg_bytes_sent   |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       0 |                  |     0 |     0 |     0 |     0 |

Detailed:
| request_path   | count   | avg_bytes_sent   | 2xx   | 3xx   | 4xx   | 5xx   |
|----------------+---------+------------------+-------+-------+-------+-------|

[exit code: 0]