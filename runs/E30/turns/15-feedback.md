$ .venv/bin/python -c "from ngxtop import config_parser; p=config_parser.build_pattern(dict(config_parser.get_log_formats(open('repro/nginx_multiline.conf').read()))['main']); print(p.pattern)"
(?P<request_time>.*) (?P<upstream_response_time>.*) (?P<remote_addr>.*) - (?P<upstream_addr>.*) \[(?P<time_local>.*)\] (?P<host>.*) "(?P<request>.*)" (?P<status>.*) (?P<bytes_sent>.*) "(?P<http_referer>.*)" "(?P<http_user_agent>.*)" "(?P<gzip_ratio>.*)" "(?P<http_x_forwarded_for>.*)" - "(?P<server_addr>.*)"

[exit code: 0]