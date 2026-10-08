Now I understand the structure. Let me look at the test_config_parser.py which got cut off, and check the README for format handling.

READ tests/test_config_parser.py

READ tests/fixtures

RUN ls -la tests/fixtures/</truncated>

Let me check the README about log_format handling and the `info` subcommand.

RUN grep -n "format" README.rst | head -50
