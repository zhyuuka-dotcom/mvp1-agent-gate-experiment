$ python3 - <<'PYEOF'
p = 'ngxtop/ngxtop.py'
s = open(p).read()

# import resolve_log_format
old_imp = "from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern"
new_imp = "from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern, resolve_log_format"
assert old_imp in s
s = s.replace(old_imp, new_imp, 1)

# resolve named format inside process()
old = """    logging.info('access_log: %s', access_log)
    logging.info('log_format: %s', log_format)"""
new = """    # `-f` may reference a log_format name defined in the nginx config
    log_format = resolve_log_format(log_format, arguments)

    logging.info('access_log: %s', access_log)
    logging.info('log_format: %s', log_format)"""
assert old in s
s = s.replace(old, new, 1)
open(p, 'w').write(s)
print("ok")
PYEOF
ok

[exit code: 0]