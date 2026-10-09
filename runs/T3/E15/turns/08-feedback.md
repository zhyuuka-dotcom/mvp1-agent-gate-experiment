$ grep -rn "avg_bytes_sent\|\"Detail\|'Detail\|Summary\|med_" tests/ && echo "===" && grep -rn "DEFAULT_QUERIES\|med_" ngxtop/
tests/test_characterization.py:28:    assert "Summary:" in r.stdout
tests/test_characterization.py:43:    assert "Summary:" in r.stdout
tests/test_debug_json_parsing.py:46:        self.assertNotIn("Detailed JSON parsing error:", log_output)
tests/test_debug_json_parsing.py:61:    def test_malformed_json_with_debug(self):
tests/test_debug_json_parsing.py:76:        self.assertNotIn("Detailed JSON parsing error:", log_output)
tests/test_debug_json_parsing.py:97:        self.assertIn("Detailed JSON parsing error:", log_output)  # INFO level message
===
ngxtop/ngxtop.py:87:DEFAULT_QUERIES = [
ngxtop/ngxtop.py:533:        report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]

[exit code: 0]