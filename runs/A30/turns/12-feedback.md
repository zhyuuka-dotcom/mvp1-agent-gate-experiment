$ .venv/bin/python -c "
from ngxtop import config_parser
for f in ['repro/nginx.conf','repro/nginx_multiline.conf']:
    cfg=open(f).read()
    print(f, dict(config_parser.get_log_formats(cfg)))
"
repro/nginx.conf {'main': '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'}
repro/nginx_multiline.conf {'main': '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'}

[exit code: 0]