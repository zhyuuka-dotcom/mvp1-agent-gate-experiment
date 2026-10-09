$ cd /repo 2>/dev/null; grep -rn "avg_bytes_sent\|median\|bytes_sent" tests/ README.rst | head -40
tests/test_config_parser.py:12:                                  "$status $body_bytes_sent '$http_referer' "
tests/test_config_parser.py:70:            'remote_addr', 'status', 'request', 'body_bytes_sent',
tests/test_parse_log.py:25:        self.assertEqual(record['body_bytes_sent'], 16818)
tests/test_parse_log.py:26:        self.assertEqual(record['bytes_sent'], 16818)
tests/test_caddy_integration.py:49:        self.assertEqual(post_record['body_bytes_sent'], 128)
tests/test_caddy_integration.py:62:            ['status', 'remote_addr', 'request', 'bytes_sent', 'status_type']
tests/test_json_extraction_fix.py:50:        self.assertEqual(records[0]['body_bytes_sent'], 47875)
README.rst:76:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:81:    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:138:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:143:    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:165:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:170:    | request_path                        |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:192:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:197:    | host                |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |

[exit code: 0]