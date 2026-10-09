[harness 注记: 存在无法解析的工具调用片段（畸形标记），已忽略]
$ grep -rn "bytes_sent\|median\|percentile\|Summary\|Detailed\|DEFAULT_QUERIES\|DEFAULT_FIELDS" tests/ | grep -v test_characterization | head -40
tests/test_config_parser.py:12:                                  "$status $body_bytes_sent '$http_referer' "
tests/test_config_parser.py:70:            'remote_addr', 'status', 'request', 'body_bytes_sent',
tests/test_parse_log.py:25:        self.assertEqual(record['body_bytes_sent'], 16818)
tests/test_parse_log.py:26:        self.assertEqual(record['bytes_sent'], 16818)
tests/test_caddy_integration.py:49:        self.assertEqual(post_record['body_bytes_sent'], 128)
tests/test_caddy_integration.py:62:            ['status', 'remote_addr', 'request', 'bytes_sent', 'status_type']
tests/test_json_extraction_fix.py:50:        self.assertEqual(records[0]['body_bytes_sent'], 47875)
tests/test_debug_json_parsing.py:45:        # Detailed debugging should NOT be present (we're at WARNING level)
tests/test_debug_json_parsing.py:46:        self.assertNotIn("Detailed JSON parsing error:", log_output)
tests/test_debug_json_parsing.py:76:        self.assertNotIn("Detailed JSON parsing error:", log_output)
tests/test_debug_json_parsing.py:97:        self.assertIn("Detailed JSON parsing error:", log_output)  # INFO level message

[exit code: 0]