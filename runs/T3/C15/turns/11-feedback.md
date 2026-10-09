$ .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f main 2>&1 | head -30; echo "==="; cat repro/access.log
/tmp/t3c15/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t3c15/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t3c15/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t3c15/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]
running for 0 seconds, 0 records processed: 0.00 req/sec

Summary:
|   count | avg_bytes_sent   |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       0 |                  |     0 |     0 |     0 |     0 |

Detailed:
| request_path   | count   | avg_bytes_sent   | 2xx   | 3xx   | 4xx   | 5xx   |
|----------------+---------+------------------+-------+-------+-------+-------|
===
0.005 0.004 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:01 +0000] example.com "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.012 0.010 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:02 +0000] example.com "GET /api HTTP/1.1" 404 153 "-" "curl/8.0" "-" "-" - "10.0.0.2"
0.003 0.002 10.0.0.1 - 192.168.1.10:8080 [06/Oct/2026:00:10:03 +0000] example.com "GET / HTTP/1.1" 200 2048 "https://example.com/" "Mozilla/5.0" "-" "-" - "10.0.0.2"
0.120 0.118 10.0.0.3 - 192.168.1.11:8080 [06/Oct/2026:00:10:04 +0000] api.example.com "GET /img/a.png HTTP/1.1" 500 512 "-" "Mozilla/5.0" "-" "-" - "10.0.0.3"
0.008 0.007 10.0.0.2 - 192.168.1.10:8080 [06/Oct/2026:00:10:05 +0000] example.com "GET /old HTTP/1.1" 301 300 "-" "curl/8.0" "-" "-" - "10.0.0.2"

[exit code: 0]