$ ls -la ngxtop repro && echo "=== ngxtop files ===" && wc -l ngxtop/*.py
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
=== ngxtop files ===
    0 ngxtop/__init__.py
  162 ngxtop/config_parser.py
  626 ngxtop/ngxtop.py
   21 ngxtop/utils.py
  809 total

[exit code: 0]