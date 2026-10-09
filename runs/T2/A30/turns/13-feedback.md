$ echo "=== stdin + json ==="; cat repro/combined.log | .venv/bin/python -m ngxtop.ngxtop -f combined --no-follow --output-format json 2>/tmp/serr; echo "stderr:"; grep running /tmp/serr
echo "=== format string direct + -g + json ==="; .venv/bin/python -m ngxtop.ngxtop -f '$remote_addr - - [$time_local] "$request" $status $bytes_sent' -l repro/combined.log --no-follow -g remote_addr --output-format json 2>/dev/null
=== stdin + json ===
{"summary": {"count": 2, "avg_bytes_sent": 2636.5, "2xx": 1, "3xx": 0, "4xx": 1, "5xx": 0}, "detailed": [{"request_path": "/api", "count": 1, "avg_bytes_sent": 153.0, "2xx": 0, "3xx": 0, "4xx": 1, "5xx": 0}, {"request_path": "/", "count": 1, "avg_bytes_sent": 5120.0, "2xx": 1, "3xx": 0, "4xx": 0, "5xx": 0}]}
stderr:
running for 0 seconds, 2 records processed: 13842.59 req/sec
=== format string direct + -g + json ===
{"summary": {"count": 0, "avg_bytes_sent": null, "2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}, "detailed": []}

[exit code: 0]