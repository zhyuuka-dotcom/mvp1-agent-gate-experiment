$ grep -rn "\.report()\|process_log\|DEFAULT_QUERIES" tests/ ngxtop/ && echo "=== baseline ===" && .venv/bin/python -m pytest tests/ -q 2>&1 | tail -5
tests/test_caddy_integration.py:75:        report = processor.report()
ngxtop/ngxtop.py:87:DEFAULT_QUERIES = [
ngxtop/ngxtop.py:490:def process_log(lines, pattern, processor, arguments):
ngxtop/ngxtop.py:502:    print(processor.report())  # this will only run when start in --no-follow mode
ngxtop/ngxtop.py:533:        report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]
ngxtop/ngxtop.py:566:        output = processor.report()
ngxtop/ngxtop.py:605:    process_log(source, pattern, processor, arguments)
=== baseline ===
  /tmp/t2a30/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:287: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    return func(*args[limit:])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.88s

[exit code: 0]