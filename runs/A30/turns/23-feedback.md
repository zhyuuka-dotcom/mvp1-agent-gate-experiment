$ tail -20 tests/test_config_parser.py
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


[exit code: 0]