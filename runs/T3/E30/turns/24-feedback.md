$ FMT=$(.venv/bin/python -c "import re;t=open('repro/nginx.conf').read();print(re.search(r\"log_format\s+main\s+'(.*?)';\",t).group(1))"); .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f "$FMT" --no-follow
running for 0 seconds, 5 records processed: 6853.44 req/sec

Summary:
|   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+---------------------+-------+-------+-------+-------|
|       5 |         1626.600 |                 512 |     2 |     1 |     1 |     1 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+---------------------+-------+-------+-------+-------|
| /              |       2 |         3584.000 |            3584.000 |     2 |     0 |     0 |     0 |
| /old           |       1 |          300.000 |             300.000 |     0 |     1 |     0 |     0 |
| /img/a.png     |       1 |          512.000 |             512.000 |     0 |     0 |     0 |     1 |
| /api           |       1 |          153.000 |             153.000 |     0 |     0 |     1 |     0 |

[stderr]
/tmp/t3e30/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
  name = re.findall('(<\S*?>)', source)[0]
/tmp/t3e30/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
  value = re.findall('\[default: (.*)\]', source, flags=re.I)
/tmp/t3e30/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
  matched = re.findall('\[default: (.*)\]', description, flags=re.I)
/tmp/t3e30/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
  split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]

[exit code: 0]