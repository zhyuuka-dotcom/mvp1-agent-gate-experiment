$ .venv/bin/python -m pytest tests/ -q 2>&1 | tail -20; echo "=== CLI ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f main 2>&1 | head -30
  /tmp/t3c30/repo/ngxtop/config_parser.py:63: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in access_log.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_access_logs_with_format_name
  /tmp/t3c30/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:290: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    ret = func(*args[limit:])

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t3c30/repo/ngxtop/config_parser.py:85: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in log_format.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t3c30/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:287: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    return func(*args[limit:])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.86s
=== CLI ===
/tmp/t3c30/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t3c30/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t3c30/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t3c30/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]
running for 0 seconds, 0 records processed: 0.00 req/sec

Summary:
|   count | avg_bytes_sent   |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       0 |                  |     0 |     0 |     0 |     0 |

Detailed:
| request_path   | count   | avg_bytes_sent   | 2xx   | 3xx   | 4xx   | 5xx   |
|----------------+---------+------------------+-------+-------+-------+-------|

[exit code: 0]