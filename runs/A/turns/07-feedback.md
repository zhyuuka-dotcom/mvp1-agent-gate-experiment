$ .venv/bin/python -m pytest tests/ -q 2>&1 | tail -20
  /home/z/my-project/learnhub/lab/mvp1/repo_frozen/ngxtop/config_parser.py:63: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in access_log.searchString(config).asList():

my-project/learnhub/lab/mvp1/repo_frozen/tests/test_config_parser.py::TestConfigParser::test_access_logs_with_format_name
  /home/z/my-project/learnhub/lab/mvp1/repo_frozen/.venv/lib/python3.12/site-packages/pyparsing/core.py:290: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    ret = func(*args[limit:])

my-project/learnhub/lab/mvp1/repo_frozen/tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /home/z/my-project/learnhub/lab/mvp1/repo_frozen/ngxtop/config_parser.py:85: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in log_format.searchString(config).asList():

my-project/learnhub/lab/mvp1/repo_frozen/tests/test_config_parser.py::TestConfigParser::test_get_log_formats
my-project/learnhub/lab/mvp1/repo_frozen/tests/test_config_parser.py::TestConfigParser::test_get_log_formats
my-project/learnhub/lab/mvp1/repo_frozen/tests/test_config_parser.py::TestConfigParser::test_get_log_formats
my-project/learnhub/lab/mvp1/repo_frozen/tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /home/z/my-project/learnhub/lab/mvp1/repo_frozen/.venv/lib/python3.12/site-packages/pyparsing/core.py:287: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    return func(*args[limit:])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.94s

[exit code: 0]