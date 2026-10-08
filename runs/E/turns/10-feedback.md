$ .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow 2>&1; echo "EXIT: $?"
/tmp/e15/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/e15/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/e15/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/e15/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]
running for 0 seconds, 0 records processed: 0.00 req/sec

Summary:
|   count | avg_bytes_sent   |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       0 |                  |     0 |     0 |     0 |     0 |

Detailed:
| request_path   | count   | avg_bytes_sent   | 2xx   | 3xx   | 4xx   | 5xx   |
|----------------+---------+------------------+-------+-------+-------+-------|
EXIT: 0

[exit code: 0]