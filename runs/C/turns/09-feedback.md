$ .venv/bin/python -c "
from ngxtop.config_parser import get_log_formats, build_pattern
cfg = open('repro/nginx.conf').read()
for name, fmt in get_log_formats(cfg):
    print('NAME:', repr(name))
    print('FMT:', repr(fmt))
    p = build_pattern(fmt)
    line = open('repro/access.log').readline().strip()
    print('MATCH:', bool(p.match(line)))
    print('PATTERN:', p.pattern)
"
NAME: 'main'
FMT: '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'
MATCH: True
PATTERN: (?P<request_time>.*) (?P<upstream_response_time>.*) (?P<remote_addr>.*) - (?P<upstream_addr>.*) \[(?P<time_local>.*)\] (?P<host>.*) "(?P<request>.*)" (?P<status>.*) (?P<bytes_sent>.*) "(?P<http_referer>.*)" "(?P<http_user_agent>.*)" "(?P<gzip_ratio>.*)" "(?P<http_x_forwarded_for>.*)" - "(?P<server_addr>.*)"

[exit code: 0]