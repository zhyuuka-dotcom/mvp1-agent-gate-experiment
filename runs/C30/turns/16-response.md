I have a clear picture. The fix: when `-f <value>` is given and the value matches a `log_format` name defined in the nginx config, resolve it to the actual format string. 

Let me design the change in `config_parser.py`: add a `resolve_log_format` function that, given a format name, looks up nginx config (using `--config` or detected path), and returns the resolved format string. Then use it in `ngxtop.py`'s `process()`.

Let me check the docopt args keys and confirm `--config` availability in `process()`.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -c "
from docopt import docopt
import ngxtop.ngxtop as n
" 2>/dev/null; grep -n "arguments\['--config'\]\|arguments\['info'\]\|build_source\|def process" ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
