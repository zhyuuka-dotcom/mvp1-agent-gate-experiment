A stray `</parameter>` got appended. Let me re-run cleanly, capturing the format via command substitution.

RUN FMT=$(.venv/bin/python -c "import re;t=open('repro/nginx.conf').read();print(re.search(r\"log_format\s+main\s+'(.*?)';\",t).group(1))"); .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f "$FMT" --no-follow

Send.
