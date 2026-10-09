$ .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' --no-follow</parameter>

[stderr]
bash: -c: line 1: syntax error near unexpected token `newline'
bash: -c: line 1: `.venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' --no-follow</parameter>'

[exit code: 2]