The parser and pattern work correctly. So when `-f main` is passed on the command line, "main" is treated literally as a format string, not as a format name. Let me check the CLI path with `-f main` and what pattern is built.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -c "
from ngxtop.config_parser import build_pattern
p = build_pattern('main')
print(repr(p.pattern))
line = open('repro/access.log').readline().strip()
print('MATCH:', p.match(line))
"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
