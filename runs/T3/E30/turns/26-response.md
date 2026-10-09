Now verify output shows 512.000.

RUN FMT=$(.venv/bin/python -c "import re;t=open('repro/nginx.conf').read();print(re.search(r\"log_format\s+main\s+'(.*?)';\",t).group(1))"); .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f "$FMT" --no-follow 2>/dev/null | grep -A4 "Summary:"

Send.
