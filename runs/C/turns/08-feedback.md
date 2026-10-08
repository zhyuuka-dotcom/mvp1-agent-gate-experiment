$ .venv/bin/python -c "
from ngxtop.config_parser import build_pattern, extract_variables, get_log_formats
fmt = \"\$request_time \$upstream_response_time \$remote_addr - \$upstream_addr [\$time_local] \$host \\\"\$request\\\" \$status \$bytes_sent \\\"\$http_referer\\\" \\\"\$http_user_agent\\\" \\\"\$gzip_ratio\\\" \\\"\$http_x_forwarded_for\\\" - \\\"\$server_addr\\\"\"
p = build_pattern(fmt)
print('PATTERN:', p.pattern)
print()
line = open('repro/access.log').readline().strip()
print('LINE:', line)
print('MATCH:', p.match(line))
print()
print('VARS:', list(extract_variables(fmt)))
"
PATTERN: (?P<request_time>.*) (?P<upstream_response_time>.*) (?P<remote_addr>.*) - (?P<upstream_addr>.*) \[(?P<time_local>.*)\] (?P<host>.*) "(?P<request>.*)" (?P<status>.*) (?P<bytes_sent>.*) "(?P<http_referer>.*)" "(?P<http_user_agent>.*)" "(?P<gzip_ratio>.*)" "(?P<http_x_forwarded_for>.*)" - "(?P<server_addr>.*)"

LINE: 0.005 0.004 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:01 +0000] example.com "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0" "-" "-" - "10.0.0.2"
MATCH: <re.Match object; span=(0, 146), match='0.005 0.004 10.0.0.1 - 192.168.1.10:8080 [06/Oct/>

VARS: ['request_time', 'upstream_response_time', 'remote_addr', 'upstream_addr', 'time_local', 'host', 'request', 'status', 'bytes_sent', 'http_referer', 'http_user_agent', 'gzip_ratio', 'http_x_forwarded_for', 'server_addr']

[exit code: 0]