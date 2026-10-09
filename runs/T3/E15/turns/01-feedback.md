$ ls -la && echo "---" && find . -type f -name "*.py" | grep -v ".venv" | head -50
total 52
drwxrwxr-x 6 z z  4096 Oct  7 05:15 .
drwxrwxr-x 4 z z  4096 Oct 10 02:59 ..
-rw-rw-r-- 1 z z    26 Oct  6 12:41 .gitignore
drwxrwxr-x 4 z z  4096 Oct  6 12:36 .venv
-rw-rw-r-- 1 z z  1076 Oct  6 12:33 LICENSE.txt
-rw-rw-r-- 1 z z 10423 Oct  6 12:33 README.rst
drwxrwxr-x 2 z z  4096 Oct  8 23:03 ngxtop
drwxrwxr-x 2 z z  4096 Oct  6 12:33 repro
-rw-rw-r-- 1 z z    21 Oct  6 12:33 setup.cfg
-rw-rw-r-- 1 z z  1084 Oct  6 12:33 setup.py
drwxrwxr-x 3 z z  4096 Oct  6 12:34 tests
---
./tests/test_config_parser.py
./tests/test_parse_log.py
./tests/test_caddy_integration.py
./tests/test_json_extraction_fix.py
./tests/test_characterization.py
./tests/test_debug_json_parsing.py
./tests/test_log_rotation.py
./setup.py
./ngxtop/utils.py
./ngxtop/__init__.py
./ngxtop/ngxtop.py
./ngxtop/config_parser.py

[exit code: 0]