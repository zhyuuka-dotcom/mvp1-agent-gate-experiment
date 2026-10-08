$ python3 - <<'PYEOF'
p = 'README.rst'
s = open(p).read()
old = "        Supported log formats: combined (default), common, caddy (for Caddy JSON access logs)\n"
new = ("        Supported log formats: combined (default), common, caddy (for Caddy JSON access logs).\n"
       "        ``-f`` may also be the name of a ``log_format`` directive defined in your nginx\n"
       "        configuration; the name is resolved using ``-c/--config`` (or the auto-detected\n"
       "        nginx config):\n\n"
       "            $ ngxtop -f main -l /var/log/nginx/access.log --no-follow -c /etc/nginx/nginx.conf\n")
assert old in s
s = s.replace(old, new, 1)
open(p, 'w').write(s)
print("ok")
PYEOF
ok

[exit code: 0]