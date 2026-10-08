$ ls -la && echo "---REPRO---" && ls -la repro/ 2>/dev/null && echo "---NGINXCONF---" && cat repro/nginx.conf 2>/dev/null && echo "---MULTILINE---" && cat repro/nginx_multiline.conf 2>/dev/null
total 52
drwxrwxr-x 6 z z  4096 Oct  7 05:15 .
drwxrwxr-x 6 z z  4096 Oct  7 05:17 ..
-rw-rw-r-- 1 z z    26 Oct  6 12:41 .gitignore
drwxrwxr-x 4 z z  4096 Oct  6 12:36 .venv
-rw-rw-r-- 1 z z  1076 Oct  6 12:33 LICENSE.txt
-rw-rw-r-- 1 z z 10423 Oct  6 12:33 README.rst
drwxrwxr-x 2 z z  4096 Oct  6 12:33 ngxtop
drwxrwxr-x 2 z z  4096 Oct  6 12:33 repro
-rw-rw-r-- 1 z z    21 Oct  6 12:33 setup.cfg
-rw-rw-r-- 1 z z  1084 Oct  6 12:33 setup.py
drwxrwxr-x 3 z z  4096 Oct  6 12:34 tests
---REPRO---
total 24
drwxrwxr-x 2 z z 4096 Oct  6 12:33 .
drwxrwxr-x 6 z z 4096 Oct  7 05:15 ..
-rw-rw-r-- 1 z z  764 Oct  6 12:33 access.log
-rw-rw-r-- 1 z z  171 Oct  6 12:33 combined.log
-rw-rw-r-- 1 z z  292 Oct  6 12:33 nginx.conf
-rw-rw-r-- 1 z z  342 Oct  6 12:33 nginx_multiline.conf
---NGINXCONF---
http {
    log_format  main  '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"';
    access_log  /var/log/nginx/access.log  main;
}
---MULTILINE---
http {
    log_format  main  '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] '
                      '$host "$request" $status $bytes_sent '
                      '"$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"';
    access_log  /var/log/nginx/access.log  main;
}

[exit code: 0]