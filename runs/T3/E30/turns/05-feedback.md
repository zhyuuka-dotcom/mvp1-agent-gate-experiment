$ ls -la; echo "=== tests ==="; ls -la tests 2>&1; echo "=== repro ==="; ls -la repro 2>&1; echo "=== python/sqlite version ==="; .venv/bin/python -c "import sqlite3; print(sqlite3.sqlite_version)"
total 52
drwxrwxr-x 6 z z  4096 Oct  7 05:15 .
drwxrwxr-x 4 z z  4096 Oct 10 03:02 ..
-rw-rw-r-- 1 z z    26 Oct  6 12:41 .gitignore
drwxrwxr-x 4 z z  4096 Oct  6 12:36 .venv
-rw-rw-r-- 1 z z  1076 Oct  6 12:33 LICENSE.txt
-rw-rw-r-- 1 z z 10423 Oct  6 12:33 README.rst
drwxrwxr-x 2 z z  4096 Oct  8 23:03 ngxtop
drwxrwxr-x 2 z z  4096 Oct  6 12:33 repro
-rw-rw-r-- 1 z z    21 Oct  6 12:33 setup.cfg
-rw-rw-r-- 1 z z  1084 Oct  6 12:33 setup.py
drwxrwxr-x 3 z z  4096 Oct  6 12:34 tests
=== tests ===
total 52
drwxrwxr-x 3 z z 4096 Oct  6 12:34 .
drwxrwxr-x 6 z z 4096 Oct  7 05:15 ..
drwxrwxr-x 2 z z 4096 Oct  6 12:33 fixtures
-rw-rw-r-- 1 z z 3183 Oct  6 12:33 test_caddy_integration.py
-rw-r--r-- 1 z z 1467 Oct  6 12:34 test_characterization.py
-rw-rw-r-- 1 z z 3157 Oct  6 12:33 test_config_parser.py
-rw-rw-r-- 1 z z 4218 Oct  6 12:33 test_debug_json_parsing.py
-rw-rw-r-- 1 z z 2327 Oct  6 12:33 test_json_extraction_fix.py
-rw-rw-r-- 1 z z 4664 Oct  6 12:33 test_log_rotation.py
-rw-rw-r-- 1 z z 4551 Oct  6 12:33 test_parse_log.py
=== repro ===
total 24
drwxrwxr-x 2 z z 4096 Oct  6 12:33 .
drwxrwxr-x 6 z z 4096 Oct  7 05:15 ..
-rw-rw-r-- 1 z z  764 Oct  6 12:33 access.log
-rw-rw-r-- 1 z z  171 Oct  6 12:33 combined.log
-rw-rw-r-- 1 z z  292 Oct  6 12:33 nginx.conf
-rw-rw-r-- 1 z z  342 Oct  6 12:33 nginx_multiline.conf
=== python/sqlite version ===
3.53.1

[exit code: 0]