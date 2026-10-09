$ echo "=== default table unchanged ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null
echo "=== explicit table identical ==="; diff <(.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null) <(.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format table 2>/dev/null) && echo SAME
echo "=== -g remote_addr json ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g remote_addr -o 'count' --output-format json 2>/dev/null
echo "=== -g remote_addr,status json ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g remote_addr,status --output-format json 2>/dev/null
echo "=== parse check ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>/dev/null | .venv/bin/python -c 'import json,sys; d=json.load(sys.stdin); print(sorted(d))'
echo "=== tests ==="; .venv/bin/python -m pytest tests/ -q 2>&1 | tail -3
=== default table unchanged ===
running for 0 seconds, 2 records processed: 12052.60 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       2 |         2636.500 |     1 |     0 |     1 |     0 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+-------+-------+-------+-------|
| /api           |       1 |          153.000 |     0 |     0 |     1 |     0 |
| /              |       1 |         5120.000 |     1 |     0 |     0 |     0 |
=== explicit table identical ===
1c1
< running for 0 seconds, 2 records processed: 11428.62 req/sec
---
> running for 0 seconds, 2 records processed: 11949.58 req/sec
=== -g remote_addr json ===
{"summary": {"count": 2, "avg_bytes_sent": 2636.5, "2xx": 1, "3xx": 0, "4xx": 1, "5xx": 0}, "detailed": [{"remote_addr": "10.0.0.2", "count": 1, "avg_bytes_sent": 153.0, "2xx": 0, "3xx": 0, "4xx": 1, "5xx": 0}, {"remote_addr": "10.0.0.1", "count": 1, "avg_bytes_sent": 5120.0, "2xx": 1, "3xx": 0, "4xx": 0, "5xx": 0}]}
=== -g remote_addr,status json ===
{"summary": {"count": 2, "avg_bytes_sent": 2636.5, "2xx": 1, "3xx": 0, "4xx": 1, "5xx": 0}, "detailed": [{"remote_addr": "10.0.0.1", "status": 200, "count": 1, "avg_bytes_sent": 5120.0, "2xx": 1, "3xx": 0, "4xx": 0, "5xx": 0}, {"remote_addr": "10.0.0.2", "status": 404, "count": 1, "avg_bytes_sent": 153.0, "2xx": 0, "3xx": 0, "4xx": 1, "5xx": 0}]}
=== parse check ===
['detailed', 'summary']
=== tests ===

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.87s

[exit code: 0]