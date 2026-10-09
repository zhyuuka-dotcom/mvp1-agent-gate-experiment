$ grep -rn "bytes_sent\|avg_bytes_sent\|median" README.rst tests/ ngxtop/ | grep -v ".venv"
README.rst:76:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:81:    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:138:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:143:    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:165:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:170:    | request_path                        |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:192:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:197:    | host                |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
tests/test_config_parser.py:12:                                  "$status $body_bytes_sent '$http_referer' "
tests/test_config_parser.py:70:            'remote_addr', 'status', 'request', 'body_bytes_sent',
tests/test_parse_log.py:25:        self.assertEqual(record['body_bytes_sent'], 16818)
tests/test_parse_log.py:26:        self.assertEqual(record['bytes_sent'], 16818)
tests/test_caddy_integration.py:49:        self.assertEqual(post_record['body_bytes_sent'], 128)
tests/test_caddy_integration.py:62:            ['status', 'remote_addr', 'request', 'bytes_sent', 'status_type']
tests/test_json_extraction_fix.py:50:        self.assertEqual(records[0]['body_bytes_sent'], 47875)
ngxtop/ngxtop.py:45:    $ ngxtop --order-by 'avg(bytes_sent) * count'
ngxtop/ngxtop.py:54:    $ ngxtop avg bytes_sent --filter 'status == 200 and request_path.startswith("foo")'
ngxtop/ngxtop.py:91:       avg(bytes_sent)                             AS avg_bytes_sent,
ngxtop/ngxtop.py:104:       avg(bytes_sent)                             AS avg_bytes_sent,
ngxtop/ngxtop.py:116:DEFAULT_FIELDS = set(['status_type', 'bytes_sent'])
ngxtop/ngxtop.py:356:                'body_bytes_sent': size,
ngxtop/ngxtop.py:366:            record['bytes_sent'] = record['body_bytes_sent']
ngxtop/ngxtop.py:424:    records = add_field('bytes_sent', lambda r: r['body_bytes_sent'], records)
ngxtop/ngxtop.py:425:    records = map_field('bytes_sent', to_int, records)
ngxtop/config_parser.py:17:                      '"$request" $status $body_bytes_sent ' \
ngxtop/config_parser.py:20:                      '"$request" $status $body_bytes_sent ' \
ngxtop/config_parser.py:156:                     'status', 'body_bytes_sent', 'http_referer', 'http_user_agent',

[exit code: 0]