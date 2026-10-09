$ head -50 tests/test_config_parser.py && echo "..." && cat repro/combined.log && echo "===ACCESS===" && cat repro/access.log
import unittest
from ngxtop import config_parser


class TestConfigParser(unittest.TestCase):

    def test_get_log_formats(self):
        config = '''
            http {
                # ubuntu default, log_format on multiple lines
                log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                                  "$status $body_bytes_sent '$http_referer' "
                                  '"$http_user_agent" "$http_x_forwarded_for"';
                # name can also be quoted, and format don't always have to
                log_format  'te st'  $remote_addr;
            }
        '''
        formats = dict(config_parser.get_log_formats(config))
        self.assertIn('main', formats)
        self.assertIn("'$http_referer'", formats['main'])
        self.assertIn('te st', formats)

    def test_get_access_logs_no_format(self):
        config = '''
                http {
                    # ubuntu default
                    access_log /var/log/nginx/access.log;
                    # syslog is a valid access log, but we can't follow it
                    access_log syslog:server=address combined;
                    # commented
                    # access_log commented;
                    server {
                        location / {
                            # has parameter with default format
                            access_log /path/to/log gzip=1;
                        }
                    }
                }
            '''
        logs = dict(config_parser.get_access_logs(config))
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs['/var/log/nginx/access.log'], 'combined')
        self.assertEqual(logs['/path/to/log'], 'combined')

    def test_access_logs_with_format_name(self):
        config = '''
                http {
                    access_log /path/to/main.log main gzip=5 buffer=32k flush=1m;
                    server {
                        access_log /path/to/test.log 'te st';
...
10.0.0.1 - - [06/Oct/2026:00:10:01 +0000] "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0"
10.0.0.2 - - [06/Oct/2026:00:10:02 +0000] "GET /api HTTP/1.1" 404 153 "-" "curl/8.0"
===ACCESS===
0.005 0.004 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:01 +0000] example.com "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.012 0.010 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:02 +0000] example.com "GET /api HTTP/1.1" 404 153 "-" "curl/8.0" "-" "-" - "10.0.0.2"
0.003 0.002 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:03 +0000] example.com "GET / HTTP/1.1" 200 2048 "https://example.com/" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.120 0.118 10.0.0.3 - 192.168.1.11:8080 [06/Oct/2026:00:10:04 +0000] api.example.com "GET /img/a.png HTTP/1.1" 500 512 "-" "Mozilla/5.0" "-" "-" - "10.0.0.3"
0.008 0.007 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:05 +0000] example.com "GET /old HTTP/1.1" 301 300 "-" "curl/8.0" "-" "-" - "10.0.0.2"

[exit code: 0]