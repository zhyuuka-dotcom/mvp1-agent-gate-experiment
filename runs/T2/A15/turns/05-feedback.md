$ cat ngxtop/utils.py && echo "===TESTS===" && ls tests/ && echo "===RUN===" && .venv/bin/python -m pytest tests/ -q 2>&1 | tail -20
import sys


def choose_one(choices, prompt):
    for idx, choice in enumerate(choices):
        print('%d. %s' % (idx + 1, choice))
    selected = None
    if sys.version[0] == '3':
        raw_input = input
    while not selected or selected <= 0 or selected > len(choices):
        selected = raw_input(prompt)
        try:
            selected = int(selected)
        except ValueError:
            selected = None
    return choices[selected - 1]


def error_exit(msg, status=1):
    sys.stderr.write('Error: %s\n' % msg)
    sys.exit(status)
===TESTS===
fixtures
test_caddy_integration.py
test_characterization.py
test_config_parser.py
test_debug_json_parsing.py
test_json_extraction_fix.py
test_log_rotation.py
test_parse_log.py
===RUN===
  /tmp/t2a15/repo/ngxtop/config_parser.py:63: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in access_log.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_access_logs_with_format_name
  /tmp/t2a15/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:290: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    ret = func(*args[limit:])

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t2a15/repo/ngxtop/config_parser.py:85: PyparsingDeprecationWarning: 'searchString' deprecated - use 'search_string'
    for directive in log_format.searchString(config).asList():

tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
tests/test_config_parser.py::TestConfigParser::test_get_log_formats
  /tmp/t2a15/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:287: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    return func(*args[limit:])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.93s

[exit code: 0]