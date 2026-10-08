$ .venv/bin/python -m ngxtop.ngxtop -f combined -l repro/combined.log --no-follow 2>/dev/null | head -8; echo "===MULTILINE==="; .venv/bin/python -c "
from ngxtop.config_parser import get_log_formats, build_pattern
cfg = open('repro/nginx_multiline.conf').read()
for name, fmt in get_log_formats(cfg):
    print('NAME:', repr(name))
    print('FMT:', repr(fmt))
    line = open('repro/access.log').readline().strip()
    print('MATCH:', bool(build_pattern(fmt).match(line)))
"
running for 0 seconds, 2 records processed: 14339.50 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       2 |         2636.500 |     1 |     0 |     1 |     0 |

Detailed:
===MULTILINE===
NAME: 'main'
FMT: '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'
MATCH: True

[exit code: 0]