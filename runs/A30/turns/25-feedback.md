$ python3 - <<'PYEOF'
p = 'ngxtop/ngxtop.py'
s = open(p).read()
old = """    -f <format>, --log-format <format>  log format as specify in log_format directive. [default: combined]
                                       Supported values: combined, common, caddy (for Caddy JSON format)"""
new = """    -f <format>, --log-format <format>  log format as specify in log_format directive. [default: combined]
                                       Supported values: combined, common, caddy (for Caddy JSON format).
                                       A log_format name defined in the nginx config can also be given
                                       (resolved using -c/--config or the detected nginx config)."""
assert old in s
s = s.replace(old, new, 1)
open(p, 'w').write(s)
print("ok")
PYEOF
ok

[exit code: 0]