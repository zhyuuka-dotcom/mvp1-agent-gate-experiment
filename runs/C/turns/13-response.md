`common` also yields 0 records on combined.log (which is expected, since combined.log has more fields). Let me test `combined`.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -m ngxtop.ngxtop -f combined -l repro/combined.log --no-follow 2>/dev/null | head -8; echo "===MULTILINE==="; .venv/bin/python -c "
from ngxtop.config_parser import get_log_formats, build_pattern
cfg = open('repro/nginx_multiline.conf').read()
for name, fmt in get_log_formats(cfg):
    print('NAME:', repr(name))
    print('FMT:', repr(fmt))
    line = open('repro/access.log').readline().strip()
    print('MATCH:', bool(build_pattern(fmt).match(line)))
"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
