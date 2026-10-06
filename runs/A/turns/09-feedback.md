$ grep -n "\-f \|log-format\|log_format\|main" README.rst | head -40
40:        -f <format>, --log-format <format>  log format as specify in log_format directive.
134:    $ ssh user@remote_server tail -f /var/log/apache2/access.log | ngxtop -f common
161:    $ ngxtop -l /var/log/caddy/access.log -f caddy
177:    | /static/css/main.css                |      17 |         1459.000 |    17 |     0 |     0 |     0 |
188:    $ ngxtop -l /var/log/caddy/access.log -f caddy --group-by host

[exit code: 0]