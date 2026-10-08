No git. That `common` behavior is inherent (combined.log lacks the x_forwarded_for field), not a regression — `common` was never intended to parse combined logs. Let me verify by reasoning: `common` pattern requires `"$http_x_forwarded_for"` at the end; combined.log ends with `"Mozilla/5.0"` with no extra field, so 0 records. This matches original behavior since I only changed named-format resolution.

Now let me add tests for the new behavior to lock it in.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">python3 - <<'PYEOF'
p = 'tests/test_config_parser.py'
s = open(p).read()

addition = '''

class TestResolveLogFormat(unittest.TestCase):
    """Tests for resolving a log_format *name* passed via -f/--log-format."""

    CONFIG = """
        http {
            log_format  main  '$request_time $remote_addr [$time_local] '
                              '$host "$request" $status $bytes_sent';
            access_log  /var/log/nginx/access.log  main;
        }
    """

    def setUp(self):
        import tempfile
        self._tmp = tempfile.NamedTemporaryFile('w', suffix='.conf', delete=False)
        self._tmp.write(self.CONFIG)
        self._tmp.close()
        self.config_path = self._tmp.name

    def tearDown(self):
        import os
        os.unlink(self.config_path)

    def test_named_format_resolved_from_config(self):
        resolved = config_parser.resolve_log_format('main', {'--config': self.config_path})
        self.assertIn('$request_time', resolved)
        self.assertIn('$host', resolved)

    def test_builtin_aliases_pass_through(self):
        for name in ('combined', 'common', 'caddy'):
            self.assertEqual(config_parser.resolve_log_format(name, {'--config': self.config_path}), name)

    def test_literal_format_string_passes_through(self):
        literal = '$remote_addr - $remote_user [$time_local] "$request"'
        self.assertEqual(config_parser.resolve_log_format(literal, {'--config': self.config_path}), literal)

    def test_unknown_name_exits(self):
        with self.assertRaises(SystemExit):
            config_parser.resolve_log_format('nope', {'--config': self.config_path})

    def test_named_format_builds_working_pattern(self):
        resolved = config_parser.resolve_log_format('main', {'--config': self.config_path})
        pattern = config_parser.build_pattern(resolved)
        self.assertIsNotNone(pattern)

'''
s = s.rstrip('\n') + addition
# ensure the __main__ block stays at the very end if present
open(p, 'w').write(s)
print("ok")
PYEOF</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
