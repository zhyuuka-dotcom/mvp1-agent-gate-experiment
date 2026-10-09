$ ls -R . 2>/dev/null | grep -v ".venv" | head -80
.:
LICENSE.txt
README.rst
ngxtop
repro
setup.cfg
setup.py
tests

./ngxtop:
__init__.py
config_parser.py
ngxtop.py
utils.py

./repro:
access.log
combined.log
nginx.conf
nginx_multiline.conf

./tests:
fixtures
test_caddy_integration.py
test_characterization.py
test_config_parser.py
test_debug_json_parsing.py
test_json_extraction_fix.py
test_log_rotation.py
test_parse_log.py

./tests/fixtures:
caddy_sample.log

[exit code: 0]