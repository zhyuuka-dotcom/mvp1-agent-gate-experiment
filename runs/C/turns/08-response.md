Now let me debug why the pattern fails to match. Let me test build_pattern with the format string.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -c "
from ngxtop.config_parser import build_pattern, extract_variables, get_log_formats
fmt = \"\$request_time \$upstream_response_time \$remote_addr - \$upstream_addr [\$time_local] \$host \\\"\$request\\\" \$status \$bytes_sent \\\"\$http_referer\\\" \\\"\$http_user_agent\\\" \\\"\$gzip_ratio\\\" \\\"\$http_x_forwarded_for\\\" - \\\"\$server_addr\\\"\"
p = build_pattern(fmt)
print('PATTERN:', p.pattern)
print()
line = open('repro/access.log').readline().strip()
print('LINE:', line)
print('MATCH:', p.match(line))
print()
print('VARS:', list(extract_variables(fmt)))
"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
