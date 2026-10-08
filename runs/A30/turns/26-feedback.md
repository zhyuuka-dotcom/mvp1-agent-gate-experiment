$ .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow -c repro/nginx.conf 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | grep "records processed"; echo "exit=$?"
running for 0 seconds, 5 records processed: 6730.27 req/sec
exit=0

[exit code: 0]