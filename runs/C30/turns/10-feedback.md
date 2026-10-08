$ .venv/bin/python -c "
from ngxtop import config_parser
p = config_parser.build_pattern('main')
print(repr(p.pattern))
import re
for line in open('repro/access.log'):
    line=line.rstrip()
    print(p.match(line))
" 2>&1 | head; echo "--- test with actual format from repro/nginx.conf (single line) ---"; .venv/bin/python -c "
from ngxtop import config_parser
conf=open('repro/nginx.conf').read()
print(dict(config_parser.get_log_formats(conf)))
print(dict(config_parser.get_access_logs(conf)))
"
'main'
None
None
None
None
None
--- test with actual format from repro/nginx.conf (single line) ---
{'main': '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'}
{'/var/log/nginx/access.log': 'main'}

[exit code: 0]