$ cd /repo 2>/dev/null; grep -n "Summary\|Detailed\|avg_bytes_sent\|report\|default" tests/test_characterization.py | head -40; echo "=== lines ==="; wc -l tests/*.py
22:def test_default_combined_top():
28:    assert "Summary:" in r.stdout
43:    assert "Summary:" in r.stdout
=== lines ===
   81 tests/test_caddy_integration.py
   43 tests/test_characterization.py
   80 tests/test_config_parser.py
  104 tests/test_debug_json_parsing.py
   53 tests/test_json_extraction_fix.py
  130 tests/test_log_rotation.py
   82 tests/test_parse_log.py
  573 total

[exit code: 0]