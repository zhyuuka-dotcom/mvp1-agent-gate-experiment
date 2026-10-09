It works: Summary median_bytes_sent = 512 (values 5120,153,2048,512,300 → sorted 153,300,512,2048,5120 → median 512). Detailed medians correct too.

Note: with odd count it returns int 512, displayed as "512" not "512.000" (tabulate floatfmt only applies to floats). That's fine and consistent with avg showing floats. To be more consistent, I could make finalize always return a float. But 512 for a single-value group appears as 512 vs avg 512.000. Since median is a "typical request size", consistency with float formatting is nicer. Let me make finalize return float for the odd case too, so tabulate shows ".000". Actually the task says match repo conventions; the avg column shows floats. I'll keep numeric (int or float) — but for uniform display, returning float is better. Let me update the odd branch to `return float(values[mid])`.

Let me patch that.

RUN .venv/bin/python -c "p='ngxtop/ngxtop.py';s=open(p).read();nl=chr(10);old='            return values[mid]'+nl;assert s.count(old)==1;s=s.replace(old,'            return float(values[mid])'+nl,1);open(p,'w').write(s);print('ok')"

Send.
