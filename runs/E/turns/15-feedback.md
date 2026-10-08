$ grep -n "log_format\|-f \|--log-format\|--config\|named\|format name" README.rst | head -40
40:        -f <format>, --log-format <format>  log format as specify in log_format directive.
58:        -c <file>, --config <file>  allow ngxtop to parse nginx config file for log format and location.
134:    $ ssh user@remote_server tail -f /var/log/apache2/access.log | ngxtop -f common
161:    $ ngxtop -l /var/log/caddy/access.log -f caddy
188:    $ ngxtop -l /var/log/caddy/access.log -f caddy --group-by host

[exit code: 0]