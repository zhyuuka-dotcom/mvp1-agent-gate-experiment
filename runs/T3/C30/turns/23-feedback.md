$ grep -n "sqlite3.connect" ngxtop/ngxtop.py; echo "---"; grep -n "LOG_FORMAT_COMBINED" ngxtop/config_parser.py | head -2; echo "---"; sed -n '15,18p' ngxtop/config_parser.py | cat -A
441:        self.conn = sqlite3.connect(':memory:')
---
16:LOG_FORMAT_COMBINED = '$remote_addr - $remote_user [$time_local] ' \
112:            return log_path, LOG_FORMAT_COMBINED
---
REGEX_LOG_FORMAT_VARIABLE = r'\$([a-zA-Z0-9\_]+)'$
LOG_FORMAT_COMBINED = '$remote_addr - $remote_user [$time_local] ' \$
                      '"$request" $status $body_bytes_sent ' \$
                      '"$http_referer" "$http_user_agent"'$

[exit code: 0]