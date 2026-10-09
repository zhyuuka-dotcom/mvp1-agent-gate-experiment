$ cd /repo 2>/dev/null; .venv/bin/python -m pytest tests/ -q 2>&1 | tail -5
  /tmp/t3a30/repo/.venv/lib/python3.12/site-packages/pyparsing/core.py:287: PyparsingDeprecationWarning: 'removeQuotes' deprecated - use 'remove_quotes'
    return func(*args[limit:])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
33 passed, 13 warnings in 1.09s

[exit code: 0]