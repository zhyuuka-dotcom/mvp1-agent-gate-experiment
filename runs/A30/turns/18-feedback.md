$ .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow -c repro/nginx.conf 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | head -20
running for 0 seconds, 5 records processed: 6584.46 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       5 |         1626.600 |     2 |     1 |     1 |     1 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+-------+-------+-------+-------|
| /              |       2 |         3584.000 |     2 |     0 |     0 |     0 |
| /old           |       1 |          300.000 |     0 |     1 |     0 |     0 |
| /img/a.png     |       1 |          512.000 |     0 |     0 |     0 |     1 |
| /api           |       1 |          153.000 |     0 |     0 |     1 |     0 |

[exit code: 0]