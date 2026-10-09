$ ls ngxtop/ && echo "===TESTS===" && ls tests/ && echo "===REPRO===" && ls repro/
__init__.py
config_parser.py
ngxtop.py
utils.py
===TESTS===
fixtures
test_caddy_integration.py
test_characterization.py
test_config_parser.py
test_debug_json_parsing.py
test_json_extraction_fix.py
test_log_rotation.py
test_parse_log.py
===REPRO===
access.log
combined.log
nginx.conf
nginx_multiline.conf

[exit code: 0]