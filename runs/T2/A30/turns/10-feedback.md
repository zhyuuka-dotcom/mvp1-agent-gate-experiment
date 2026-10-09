$ echo "=== EX1 stdout ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>/tmp/e1; echo "--- stderr:"; cat /tmp/e1
echo "=== EX2 stdout ==="; .venv/bin/python -m ngxtop.ngxtop -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' -l repro/access.log --no-follow --output-format json 2>/tmp/e2; echo "--- stderr:"; cat /tmp/e2
echo "=== EX3 ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml >/tmp/o3 2>/tmp/e3; echo "exit=$?"; echo "stdout:[$(cat /tmp/o3)]"; echo "stderr:[$(cat /tmp/e3)]"
=== EX1 stdout ===
{"summary": {"count": 2, "avg_bytes_sent": 2636.5, "2xx": 1, "3xx": 0, "4xx": 1, "5xx": 0}, "detailed": [{"request_path": "/api", "count": 1, "avg_bytes_sent": 153.0, "2xx": 0, "3xx": 0, "4xx": 1, "5xx": 0}, {"request_path": "/", "count": 1, "avg_bytes_sent": 5120.0, "2xx": 1, "3xx": 0, "4xx": 0, "5xx": 0}]}
--- stderr:
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]
running for 0 seconds, 2 records processed: 14051.27 req/sec
=== EX2 stdout ===
{"summary": {"count": 5, "avg_bytes_sent": 1626.6, "2xx": 2, "3xx": 1, "4xx": 1, "5xx": 1}, "detailed": [{"request_path": "/", "count": 2, "avg_bytes_sent": 3584.0, "2xx": 2, "3xx": 0, "4xx": 0, "5xx": 0}, {"request_path": "/old", "count": 1, "avg_bytes_sent": 300.0, "2xx": 0, "3xx": 1, "4xx": 0, "5xx": 0}, {"request_path": "/img/a.png", "count": 1, "avg_bytes_sent": 512.0, "2xx": 0, "3xx": 0, "4xx": 0, "5xx": 1}, {"request_path": "/api", "count": 1, "avg_bytes_sent": 153.0, "2xx": 0, "3xx": 0, "4xx": 1, "5xx": 0}]}
--- stderr:
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]
running for 0 seconds, 5 records processed: 6318.63 req/sec
=== EX3 ===
exit=2
stdout:[]
stderr:[/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t2a30/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]
Error: invalid output format "yaml" (expected: table, json)]

[exit code: 0]