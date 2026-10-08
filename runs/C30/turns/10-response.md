Now let me understand the core issue. When `-f main` is passed, it's used directly as a format string. Let me check the build_pattern with `main`:

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -c "
from ngxtop import config_parser
p = config_parser.build_pattern('main')
print(repr(p.pattern))
import re
for line in open('repro/access.log'):
    line=line.rstrip()
    print(p.match(line))
" 2>&1 | head; echo "--- test with actual format from repro/nginx.conf (single line) ---"; .venv/bin/python -c "
from ngxtop import config_parser
conf=open('repro/nginx.conf').read()
print(dict(config_parser.get_log_formats(conf)))
print(dict(config_parser.get_access_logs(conf)))
"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
