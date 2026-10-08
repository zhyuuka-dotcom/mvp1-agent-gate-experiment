The config parser correctly parses `main` when reading the config file. But when the user passes `-f main` directly on the command line, ngxtop treats "main" as a literal format string instead of resolving the named format from the nginx config.

Let me verify `-c` (config) works and what happens with `-f main -c repro/nginx.conf`:

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -m ngxtop.ngxtop -f main -c repro/nginx.conf --no-follow 2>&1 | grep -v SyntaxWarning | grep -v "re.findall\|re.split\|name =\|value =\|matched =\|split =" | head -20; echo "EXIT=${PIPESTATUS[0]}"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
