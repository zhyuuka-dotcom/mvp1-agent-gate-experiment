$ FMT=$(.venv/bin/python -c "import re;t=open('repro/nginx.conf').read();print(re.search(r\"log_format\s+main\s+'(.*?)';\",t).group(1))"); .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f "$FMT" --no-follow 2>/dev/null | grep -A4 "Summary:"
Summary:
|   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+---------------------+-------+-------+-------+-------|
|       5 |         1626.600 |             512.000 |     2 |     1 |     1 |     1 |


[exit code: 0]