Interesting - the pattern itself matches when built from the raw format string. So the issue is in how the format string is assembled/parsed. Let me check what `get_log_formats` produces from the config file (the format string passed via `-f main`).

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -c "
from ngxtop.config_parser import get_log_formats, build_pattern
cfg = open('repro/nginx.conf').read()
for name, fmt in get_log_formats(cfg):
    print('NAME:', repr(name))
    print('FMT:', repr(fmt))
    p = build_pattern(fmt)
    line = open('repro/access.log').readline().strip()
    print('MATCH:', bool(p.match(line)))
    print('PATTERN:', p.pattern)
"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
