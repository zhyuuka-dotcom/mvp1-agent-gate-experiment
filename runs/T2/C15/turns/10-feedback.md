$ 
sed -n '60,100p' tests/test_caddy_integration.py | grep -n ""; echo "==="; .venv/bin/python -m pytest tests/ -q 2>&1 | tail -15
1:        processor = ngxtop.SQLProcessor(
2:            [('Test', 'SELECT status, COUNT(*) as count FROM log GROUP BY status')],
3:            ['status', 'remote_addr', 'request', 'bytes_sent', 'status_type']
4:        )
5:        
6:        # Parse the log file
7:        pattern = build_pattern('caddy')
8:        with open(self.log_file, 'r') as f:
9:            lines = f.readlines()
10:            records = ngxtop.parse_log(lines, pattern)
11:            
12:            # Process the records
13:            processor.process(records)
14:        
15:        # Get the report and verify the results
16:        report = processor.report()
17:        self.assertIn('running for', report)
18:        self.assertIn('200', report)
19:        self.assertIn('404', report)
20:
21:
22:if __name__ == '__main__':
23:    unittest.main()
===
    ret = func(*args[limit:])

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t2c15/repo/ngxtop/config_parser.py:85: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in log_format.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t2c15/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:287: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    return func(*args[limit:])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.87s

[exit code: 0]