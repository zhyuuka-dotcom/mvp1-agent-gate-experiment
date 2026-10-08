Now let me understand the issue. When user passes `-f main`, they give the format NAME, not the format string. Let me check what `build_pattern('main')` produces.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -c "
from ngxtop.config_parser import build_pattern
p = build_pattern('main')
print(p.pattern)
"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
