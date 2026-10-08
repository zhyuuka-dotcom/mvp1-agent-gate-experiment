$ python3 - <<'PYEOF'
p = 'tests/test_config_parser.py'
s = open(p).read()
block = "\n\nif __name__ == '__main__':\n    unittest.main()\n"
# remove it wherever it sits
s = s.replace(block, "\n")
s = s.rstrip('\n') + "\n\n\nif __name__ == '__main__':\n    unittest.main()\n"
open(p, 'w').write(s)
print("ok")
PYEOF
.venv/bin/python -m pytest tests/test_config_parser.py -q 2>&1 | tail -3
ok

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
10 passed, 18 warnings in 0.11s

[exit code: 0]