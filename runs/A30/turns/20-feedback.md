$ .venv/bin/python -m ngxtop.ngxtop -f combined -l repro/combined.log --no-follow 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | grep "records processed"
.venv/bin/python -m ngxtop.ngxtop -f common -l repro/combined.log --no-follow 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | grep "records processed"
echo "----tests----"
.venv/bin/python -m pytest tests/ -q 2>&1 | tail -3
running for 0 seconds, 2 records processed: 16100.98 req/sec
running for 0 seconds, 0 records processed: 0.00 req/sec
----tests----

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
28 passed, 13 warnings in 0.83s

[exit code: 0]