$ find . -type f -not -path './.git/*' -not -path './.venv/*' | head -50
./setup.cfg
./LICENSE.txt
./repro/combined.log
./repro/access.log
./repro/nginx.conf
./repro/nginx_multiline.conf
./tests/test_config_parser.py
./tests/test_parse_log.py
./tests/test_caddy_integration.py
./tests/test_json_extraction_fix.py
./tests/test_characterization.py
./tests/test_debug_json_parsing.py
./tests/fixtures/caddy_sample.log
./tests/test_log_rotation.py
./setup.py
./.gitignore
./ngxtop/utils.py
./ngxtop/__init__.py
./ngxtop/ngxtop.py
./ngxtop/config_parser.py
./README.rst

[exit code: 0]