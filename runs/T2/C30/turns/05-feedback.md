$ .venv/bin/python -m pytest tests/ -q 2>&1 | tail -20
  /tmp/t2c30/repo/ngxtop/config_parser.py:63: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in access_log.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_access_logs_with_format_name
  /tmp/t2c30/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:290: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    ret = func(*args[limit:])

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t2c30/repo/ngxtop/config_parser.py:85: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in log_format.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t2c30/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:287: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    return func(*args[limit:])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.88s

[exit code: 0]