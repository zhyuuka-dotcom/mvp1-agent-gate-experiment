$ mkdir -p /tmp/fakebin
cat > /tmp/fakebin/nginx <<'EOF'
#!/bin/sh
echo "nginx version: nginx/1.18.0" >&2
echo "configure arguments: --conf-path=/tmp/r2a30/repo/repro/nginx.conf" >&2
EOF
chmod +x /tmp/fakebin/nginx
PATH=/tmp/fakebin:$PATH .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow 2>&1 | grep -v "SyntaxWarning\|re.findall\|re.split\|name = \|value = \|matched = \|split = " | grep "records processed"
running for 0 seconds, 5 records processed: 5750.35 req/sec

[exit code: 0]