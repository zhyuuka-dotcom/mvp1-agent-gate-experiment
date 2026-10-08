$ ls -la ngxtop/ && echo "=== repro/nginx.conf ===" && cat repro/nginx.conf && echo "=== repro/nginx_multiline.conf ===" && cat repro/nginx_multiline.conf && echo "=== repro/access.log ===" && cat repro/access.log && echo "=== repro/combined.log ===" && cat repro/combined.log
total 44
drwxrwxr-x 2 z z  4096 Oct  8 23:03 .
drwxrwxr-x 6 z z  4096 Oct  7 05:15 ..
-rw-rw-r-- 1 z z     0 Oct  6 12:33 __init__.py
-rw-rw-r-- 1 z z  6032 Oct  8 23:03 config_parser.py
-rw-rw-r-- 1 z z 23519 Oct  6 12:33 ngxtop.py
-rw-rw-r-- 1 z z   548 Oct  6 12:33 utils.py
=== repro/nginx.conf ===
http {
    log_format  main  '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"';
    access_log  /var/log/nginx/access.log  main;
}
=== repro/nginx_multiline.conf ===
http {
    log_format  main  '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] '
                      '$host "$request" $status $bytes_sent '
                      '"$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"';
    access_log  /var/log/nginx/access.log  main;
}
=== repro/access.log ===
0.005 0.004 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:01 +0000] example.com "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.012 0.010 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:02 +0000] example.com "GET /api HTTP/1.1" 404 153 "-" "curl/8.0" "-" "-" - "10.0.0.2"
0.003 0.002 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:03 +0000] example.com "GET / HTTP/1.1" 200 2048 "https://example.com/" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.120 0.118 10.0.0.3 - 192.168.1.11:8080 [06/Oct/2026:00:10:04 +0000] api.example.com "GET /img/a.png HTTP/1.1" 500 512 "-" "Mozilla/5.0" "-" "-" - "10.0.0.3"
0.008 0.007 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:05 +0000] example.com "GET /old HTTP/1.1" 301 300 "-" "curl/8.0" "-" "-" - "10.0.0.2"
=== repro/combined.log ===
10.0.0.1 - - [06/Oct/2026:00:10:01 +0000] "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0"
10.0.0.2 - - [06/Oct/2026:00:10:02 +0000] "GET /api HTTP/1.1" 404 153 "-" "curl/8.0"

[exit code: 0]