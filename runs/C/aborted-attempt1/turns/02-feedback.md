$ cat repro/access.log && echo "---COMBINED---" && cat repro/combined.log && echo "---LS NGXTOP---" && ls -la ngxtop/ && echo "---LS TESTS---" && ls -la tests/
0.005 0.004 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:01 +0000] example.com "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.012 0.010 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:02 +0000] example.com "GET /api HTTP/1.1" 404 153 "-" "curl/8.0" "-" "-" - "10.0.0.2"
0.003 0.002 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:03 +0000] example.com "GET / HTTP/1.1" 200 2048 "https://example.com/" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.120 0.118 10.0.0.3 - 192.168.1.11:8080 [06/Oct/2026:00:10:04 +0000] api.example.com "GET /img/a.png HTTP/1.1" 500 512 "-" "Mozilla/5.0" "-" "-" - "10.0.0.3"
0.008 0.007 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:05 +0000] example.com "GET /old HTTP/1.1" 301 300 "-" "curl/8.0" "-" "-" - "10.0.0.2"
---COMBINED---
10.0.0.1 - - [06/Oct/2026:00:10:01 +0000] "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0"
10.0.0.2 - - [06/Oct/2026:00:10:02 +0000] "GET /api HTTP/1.1" 404 153 "-" "curl/8.0"
---LS NGXTOP---
total 44
drwxrwxr-x 2 z z  4096 Oct  6 12:33 .
drwxrwxr-x 6 z z  4096 Oct  7 05:15 ..
-rw-rw-r-- 1 z z     0 Oct  6 12:33 __init__.py
-rw-rw-r-- 1 z z  7826 Oct  7 05:22 config_parser.py
-rw-rw-r-- 1 z z 23519 Oct  6 12:33 ngxtop.py
-rw-rw-r-- 1 z z   548 Oct  6 12:33 utils.py
---LS TESTS---
total 52
drwxrwxr-x 3 z    z    4096 Oct  6 12:34 .
drwxrwxr-x 6 z    z    4096 Oct  7 05:15 ..
drwxrwxr-x 2 z    z    4096 Oct  6 12:33 fixtures
-rw-rw-r-- 1 z    z    3183 Oct  6 12:33 test_caddy_integration.py
-rw-r--r-- 1 root root 1467 Oct  6 12:34 test_characterization.py
-rw-rw-r-- 1 z    z    3157 Oct  6 12:33 test_config_parser.py
-rw-rw-r-- 1 z    z    4218 Oct  6 12:33 test_debug_json_parsing.py
-rw-rw-r-- 1 z    z    2327 Oct  6 12:33 test_json_extraction_fix.py
-rw-rw-r-- 1 z    z    4664 Oct  6 12:33 test_log_rotation.py
-rw-rw-r-- 1 z    z    4551 Oct  6 12:33 test_parse_log.py

[exit code: 0]