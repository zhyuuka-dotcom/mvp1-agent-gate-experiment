$ .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow -c repro/nginx_multiline.conf 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | grep "records processed"
echo "----info----"
.venv/bin/python -m ngxtop.ngxtop info -f main -l repro/access.log -c repro/nginx.conf 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = "
echo "----bad name----"
.venv/bin/python -m ngxtop.ngxtop -f doesnotexist -l repro/access.log --no-follow -c repro/nginx.conf 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = "; echo "exit=$?"
running for 0 seconds, 5 records processed: 6590.67 req/sec
----info----
Usage:
    ngxtop [options]
    ngxtop [options] (print|top|avg|sum) <var> ...
    ngxtop info
    ngxtop [options] query <query> ...
----bad name----
Error: Unknown log format "doesnotexist". It is neither a built-in format (combined, common, caddy) nor a log_format name found in the nginx configuration. Use -c/--config to point ngxtop at your nginx config, or pass the full format string via -f.
exit=0

[exit code: 0]