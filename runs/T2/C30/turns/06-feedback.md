$ .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/tmp/err.txt; echo "EXIT=$?"; echo "=== STDERR ==="; cat /tmp/err.txt
running for 0 seconds, 2 records processed: 12671.61 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       2 |         2636.500 |     1 |     0 |     1 |     0 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+-------+-------+-------+-------|
| /api           |       1 |          153.000 |     0 |     0 |     1 |     0 |
| /              |       1 |         5120.000 |     1 |     0 |     0 |     0 |
EXIT=0
=== STDERR ===
/tmp/t2c30/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t2c30/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t2c30/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t2c30/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]

[exit code: 0]