$ python3 -c "p='ngxtop/ngxtop.py'; s=open(p).read(); s=s.replace('import tabulate','import tabulate  # MARKER_TEST',1); open(p,'w').write(s)"; grep -c "MARKER_TEST" ngxtop/ngxtop.py
1

[exit code: 0]