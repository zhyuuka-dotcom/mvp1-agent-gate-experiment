$ sed -n 60,90p tests/test_caddy_integration.py && echo === && cat repro/combined.log && echo === && cat repro/access.log
        processor = ngxtop.SQLProcessor(
            [('Test', 'SELECT status, COUNT(*) as count FROM log GROUP BY status')],
            ['status', 'remote_addr', 'request', 'bytes_sent', 'status_type']
        )
        
        # Parse the log file
        pattern = build_pattern('caddy')
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
            records = ngxtop.parse_log(lines, pattern)
            
            # Process the records
            processor.process(records)
        
        # Get the report and verify the results
        report = processor.report()
        self.assertIn('running for', report)
        self.assertIn('200', report)
        self.assertIn('404', report)


if __name__ == '__main__':
    unittest.main()===
10.0.0.1 - - [06/Oct/2026:00:10:01 +0000] "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0"
10.0.0.2 - - [06/Oct/2026:00:10:02 +0000] "GET /api HTTP/1.1" 404 153 "-" "curl/8.0"
===
0.005 0.004 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:01 +0000] example.com "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.012 0.010 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:02 +0000] example.com "GET /api HTTP/1.1" 404 153 "-" "curl/8.0" "-" "-" - "10.0.0.2"
0.003 0.002 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:03 +0000] example.com "GET / HTTP/1.1" 200 2048 "https://example.com/" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.120 0.118 10.0.0.3 - 192.168.1.11:8080 [06/Oct/2026:00:10:04 +0000] api.example.com "GET /img/a.png HTTP/1.1" 500 512 "-" "Mozilla/5.0" "-" "-" - "10.0.0.3"
0.008 0.007 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:05 +0000] example.com "GET /old HTTP/1.1" 301 300 "-" "curl/8.0" "-" "-" - "10.0.0.2"

[exit code: 0]