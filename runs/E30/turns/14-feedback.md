$ .venv/bin/python -c "from ngxtop import config_parser; import json; print(json.dumps(dict(config_parser.get_log_formats(open('repro/nginx_multiline.conf').read())), indent=1))"
{
 "main": "$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host \"$request\" $status $bytes_sent \"$http_referer\" \"$http_user_agent\" \"$gzip_ratio\" \"$http_x_forwarded_for\" - \"$server_addr\""
}

[exit code: 0]