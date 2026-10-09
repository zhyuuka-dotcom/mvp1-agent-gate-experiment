$ .venv/bin/python -c "p='ngxtop/ngxtop.py';s=open(p).read();nl=chr(10);old='            return values[mid]'+nl;assert s.count(old)==1;s=s.replace(old,'            return float(values[mid])'+nl,1);open(p,'w').write(s);print('ok')"
ok

[exit code: 0]