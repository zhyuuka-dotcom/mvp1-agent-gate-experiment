$ cat ngxtop/utils.py && echo "=== TESTS ===" && grep -rn "report\|output.format\|print(processor" tests/ | head -40
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
=== TESTS ===
tests/test_caddy_integration.py:74:        # Get the report and verify the results
tests/test_caddy_integration.py:75:        report = processor.report()
tests/test_caddy_integration.py:76:        self.assertIn('running for', report)
tests/test_caddy_integration.py:77:        self.assertIn('200', report)
tests/test_caddy_integration.py:78:        self.assertIn('404', report)

[exit code: 0]