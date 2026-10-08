$ cat tests/test_config_parser.py && echo "===CHAR===" && cat tests/test_characterization.py
import unittest
from ngxtop import config_parser


class TestConfigParser(unittest.TestCase):

    def test_get_log_formats(self):
        config = '''
            http {
                # ubuntu default, log_format on multiple lines
                log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                                  "$status $body_bytes_sent '$http_referer' "
                                  '"$http_user_agent" "$http_x_forwarded_for"';
                # name can also be quoted, and format don't always have to
                log_format  'te st'  $remote_addr;
            }
        '''
        formats = dict(config_parser.get_log_formats(config))
        self.assertIn('main', formats)
        self.assertIn("'$http_referer'", formats['main'])
        self.assertIn('te st', formats)

    def test_get_access_logs_no_format(self):
        config = '''
                http {
                    # ubuntu default
                    access_log /var/log/nginx/access.log;
                    # syslog is a valid access log, but we can't follow it
                    access_log syslog:server=address combined;
                    # commented
                    # access_log commented;
                    server {
                        location / {
                            # has parameter with default format
                            access_log /path/to/log gzip=1;
                        }
                    }
                }
            '''
        logs = dict(config_parser.get_access_logs(config))
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs['/var/log/nginx/access.log'], 'combined')
        self.assertEqual(logs['/path/to/log'], 'combined')

    def test_access_logs_with_format_name(self):
        config = '''
                http {
                    access_log /path/to/main.log main gzip=5 buffer=32k flush=1m;
                    server {
                        access_log /path/to/test.log 'te st';
                    }
                }
            '''
        logs = dict(config_parser.get_access_logs(config))
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs['/path/to/main.log'], 'main')
        self.assertEqual(logs['/path/to/test.log'], 'te st')

    def test_build_pattern_caddy_format(self):
        """Test that build_pattern correctly handles the 'caddy' format."""
        pattern = config_parser.build_pattern('caddy')
        self.assertEqual(pattern, 'caddy')  # For caddy, we return the string 'caddy' not a regex pattern

    def test_extract_variables_caddy_format(self):
        """Test that extract_variables returns the expected fields for caddy format."""
        variables = list(config_parser.extract_variables('caddy'))

        # Check that all expected fields are present
        expected_fields = [
            'remote_addr', 'status', 'request', 'body_bytes_sent',
            'http_referer', 'http_user_agent', 'request_time', 'request_path',
            'host'
        ]

        for field in expected_fields:
            self.assertIn(field, variables)


if __name__ == '__main__':
    unittest.main()
===CHAR===
"""特征化测试：固化文档记载的既有公开行为（MVP-1 冻结件）。

每条断言的规格出处见各测试的 provenance 注释。
这些测试在 T1 任务开始前即为绿；任何实现修改不得使其变红。
"""
import os
import subprocess
from pathlib import Path

REPO = Path(os.environ.get("MVP1_REPO", Path(__file__).resolve().parent.parent))
PY = REPO / ".venv/bin/python"
FIX = REPO / "repro"


def run_cli(*args):
    return subprocess.run(
        [str(PY), "-m", "ngxtop.ngxtop", *args],
        capture_output=True, text=True, cwd=str(REPO), timeout=60,
    )


def test_default_combined_top():
    # provenance: docopt usage（ngxtop.py 顶部 Usage 块）默认格式 combined；
    # README §Usage 基本用法 `$ ngxtop`。
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow")
    assert r.returncode == 0
    assert "2 records processed" in r.stdout
    assert "Summary:" in r.stdout


def test_group_by_single_column():
    # provenance: README/docopt 示例 `$ ngxtop --group-by remote_addr`。
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow", "-g", "remote_addr")
    assert r.returncode == 0
    assert "remote_addr" in r.stdout
    assert "10.0.0.1" in r.stdout


def test_order_by_count():
    # provenance: docopt usage `-o, --order-by` 选项。
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow", "-o", "count")
    assert r.returncode == 0
    assert "Summary:" in r.stdout

[exit code: 0]