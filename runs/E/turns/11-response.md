Reproduced: 0 records. The user passed `-f main` where `main` is a *named* format, not a format string. ngxtop treats it as a literal pattern string matching "main". Let me investigate how format resolution works and what tests exist.

READ tests/test_config_parser.py

READ tests/test_characterization.py
