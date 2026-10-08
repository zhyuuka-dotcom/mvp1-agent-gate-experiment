Interesting - the config-based path also fails! It tries to use `follow` since no `--no-follow`, but it detected access_log `/var/log/nginx/access.log` (which doesn't exist). Actually it detected the config, found `/var/log/nginx/access.log` as the path (not our repro log). Let me use `--config` with `-l`... but that's the issue.

Let me directly test the parsing logic to understand the real bug. Let me test `get_log_formats` and `detect_log_config` behavior with the multiline config.

RUN .venv/bin/python -c "from ngxtop import config_parser; import json; print(json.dumps(dict(config_parser.get_log_formats(open('repro/nginx_multiline.conf').read())), indent=1))"
