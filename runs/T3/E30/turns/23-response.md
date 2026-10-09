The format string has `$bytes_sent`. The access.log has 15+ fields. Let me pass the actual format string with `-f`. I'll extract it from nginx.conf and run the CLI.

RUN .venv/bin/python -c "import re; t=open('repro/nginx.conf').read(); m=re.search(r\"log_format\s+main\s+'(.*?)';\", t); print(m.group(1))"

Then run CLI with that format string.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' --no-follow

Send.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' --no-follow</parameter>

Send.
