5 records processed now. Test with the multiline config too, and with `info`.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">.venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow -c repro/nginx_multiline.conf 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | grep "records processed"
echo "----info----"
.venv/bin/python -m ngxtop.ngxtop info -f main -l repro/access.log -c repro/nginx.conf 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = "
echo "----bad name----"
.venv/bin/python -m ngxtop.ngxtop -f doesnotexist -l repro/access.log --no-follow -c repro/nginx.conf 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = "; echo "exit=$?"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
