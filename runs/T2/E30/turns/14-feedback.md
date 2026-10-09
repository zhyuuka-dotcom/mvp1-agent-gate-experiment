$ .venv/bin/python -m pytest tests/ -q
............................                                             [100%]
=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/docopt.py:165
  /tmp/t2e30/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
    name = re.findall('(<\S*?>)', source)[0]

.venv/lib/python3.12/site-packages/docopt.py:166
  /tmp/t2e30/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
    value = re.findall('\[default: (.*)\]', source, flags=re.I)

.venv/lib/python3.12/site-packages/docopt.py:207
  /tmp/t2e30/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
    matched = re.findall('\[default: (.*)\]', description, flags=re.I)

.venv/lib/python3.12/site-packages/docopt.py:456
  /tmp/t2e30/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
    split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]

ngxtop/config_parser.py:29
  /tmp/t2e30/repo/ngxtop/config_parser.py:29: PyparsingDeprecationWarning: 'setParseAction' deprecated - use 'set_parse_action'
    parameter = parameter | quotedString.setParseAction(removeQuotes)

tests/test_config_parser.py::TestConfigParser::test_access_logs_with_format_name
tests/test_config_parser.py::TestConfigParser::test_get_access_logs_no_format
  /tmp/t2e30/repo/ngxtop/config_parser.py:63: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in access_log.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_access_logs_with_format_name
  /tmp/t2e30/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:290: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    ret = func(*args[limit:])

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t2e30/repo/ngxtop/config_parser.py:85: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in log_format.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t2e30/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:287: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    return func(*args[limit:])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.88s

[exit code: 0]