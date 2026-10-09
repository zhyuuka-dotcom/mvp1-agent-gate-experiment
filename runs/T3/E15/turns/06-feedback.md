$ .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow && echo "=====ACCESS NO-FOLLOW=====" && .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f "$(cat repro/nginx.conf | grep log_format | sed "s/.*log_format *main *//; s/';.*//; s/'//g")" --no-follow 2>&1 | head -30
running for 0 seconds, 2 records processed: 11199.74 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       2 |         2636.500 |     1 |     0 |     1 |     0 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+-------+-------+-------+-------|
| /api           |       1 |          153.000 |     0 |     0 |     1 |     0 |
| /              |       1 |         5120.000 |     1 |     0 |     0 |     0 |
=====ACCESS NO-FOLLOW=====
/tmp/t3e15/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t3e15/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t3e15/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t3e15/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]
running for 0 seconds, 5 records processed: 3867.86 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       5 |         1626.600 |     2 |     1 |     1 |     1 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+-------+-------+-------+-------|
| /              |       2 |         3584.000 |     2 |     0 |     0 |     0 |
| /old           |       1 |          300.000 |     0 |     1 |     0 |     0 |
| /img/a.png     |       1 |          512.000 |     0 |     0 |     0 |     1 |
| /api           |       1 |          153.000 |     0 |     0 |     1 |     0 |

[stderr]
/tmp/t3e15/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t3e15/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t3e15/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t3e15/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]

[exit code: 0]