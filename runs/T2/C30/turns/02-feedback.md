$ ls -la ngxtop/ tests/; echo "==="; wc -l ngxtop/*.py tests/*.py
ngxtop/:
total 44
drwxrwxr-x 2 z z  4096 Oct  8 23:03 .
drwxrwxr-x 6 z z  4096 Oct  7 05:15 ..
-rw-rw-r-- 1 z z     0 Oct  6 12:33 __init__.py
-rw-rw-r-- 1 z z  6032 Oct  8 23:03 config_parser.py
-rw-rw-r-- 1 z z 23519 Oct  6 12:33 ngxtop.py
-rw-rw-r-- 1 z z   548 Oct  6 12:33 utils.py

tests/:
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
===
    0 ngxtop/__init__.py
  162 ngxtop/config_parser.py
  626 ngxtop/ngxtop.py
   21 ngxtop/utils.py
   81 tests/test_caddy_integration.py
   43 tests/test_characterization.py
   80 tests/test_config_parser.py
  104 tests/test_debug_json_parsing.py
   53 tests/test_json_extraction_fix.py
  130 tests/test_log_rotation.py
   82 tests/test_parse_log.py
 1382 total

[exit code: 0]