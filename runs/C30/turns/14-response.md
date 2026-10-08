<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">.venv/bin/python -c "
from ngxtop import config_parser
conf=open('repro/nginx.conf').read()
fmts=dict(config_parser.get_log_formats(conf))
fmt=fmts['main']
p=config_parser.build_pattern(fmt)
n=0
for line in open('repro/access.log'):
    m=p.match(line.rstrip())
    if m: n+=1
    else: print('NO MATCH:', line[:60])
print('matched lines:', n)
"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
