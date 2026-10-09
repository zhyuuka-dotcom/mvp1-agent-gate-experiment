All three examples match the expected outputs exactly. The docopt SyntaxWarnings on stderr are pre-existing environment noise (present on baseline too), not JSON output. Let me verify that.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ parameter name="command" string="true">echo "=== default table unchanged ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null
echo "=== explicit table identical ==="; diff <(.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null) <(.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format table 2>/dev/null) && echo SAME
echo "=== -g remote_addr json ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g remote_addr --output-format json 2>/dev/null
echo "=== -g remote_addr,status json ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g remote_addr,status --output-format json 2>/dev/null
echo "=== json only one doc (parse check) ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>/dev/null | .venv/bin/python -c 'import json,sys; d=json.load(sys.stdin); print(sorted(d))'
echo "=== tests ==="; .venv/bin/python -m pytest tests/ -q 2>&1 | tail -3</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
