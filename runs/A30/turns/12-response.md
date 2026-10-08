Let me also reproduce the exact issue command from the report, which uses `-f main` alongside `-l`. I already did. Let me also check the `--config` interplay and how the multiline format is parsed (directive join).

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">.venv/bin/python -c "
from ngxtop import config_parser
for f in ['repro/nginx.conf','repro/nginx_multiline.conf']:
    cfg=open(f).read()
    print(f, dict(config_parser.get_log_formats(cfg)))
"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
