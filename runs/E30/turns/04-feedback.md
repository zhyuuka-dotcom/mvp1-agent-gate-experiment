$ ls -la ngxtop repro tests
ngxtop:
total 44
drwxrwxr-x 2 z z  4096 Oct  8 23:03 .
drwxrwxr-x 6 z z  4096 Oct  7 05:15 ..
-rw-rw-r-- 1 z z     0 Oct  6 12:33 __init__.py
-rw-rw-r-- 1 z z  6032 Oct  8 23:03 config_parser.py
-rw-rw-r-- 1 z z 23519 Oct  6 12:33 ngxtop.py
-rw-rw-r-- 1 z z   548 Oct  6 12:33 utils.py

repro:
total 24
drwxrwxr-x 2 z z 4096 Oct  6 12:33 .
drwxrwxr-x 6 z z 4096 Oct  7 05:15 ..
-rw-rw-r-- 1 z z  764 Oct  6 12:33 access.log
-rw-rw-r-- 1 z z  171 Oct  6 12:33 combined.log
-rw-rw-r-- 1 z z  292 Oct  6 12:33 nginx.conf
-rw-rw-r-- 1 z z  342 Oct  6 12:33 nginx_multiline.conf

tests:
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

[exit code: 0]