Multiline works, bad name errors clearly. `info` doesn't accept `-f` (it worked earlier as `ngxtop info` with no options) — not important. Now verify built-in aliases and caddy still work, and run the test suite.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">.venv/bin/python -m ngxtop.ngxtop -f combined -l repro/combined.log --no-follow 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | grep "records processed"
.venv/bin/python -m ngxtop.ngxtop -f common -l repro/combined.log --no-follow 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | grep "records processed"
echo "----tests----"
.venv/bin/python -m pytest tests/ -q 2>&1 | tail -3</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
