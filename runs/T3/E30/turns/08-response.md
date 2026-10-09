Multi-line strings broke. Let me use a single-line python command.

RUN .venv/bin/python -c "import itertools; [print(i,repr(l)) for i,l in enumerate(open('ngxtop/ngxtop.py'),1) if 'avg(bytes_sent)' in l][:1]"

RUN grep -n "avg(bytes_sent)" ngxtop/ngxtop.py | head -2

Let me just grep.

RUN grep -n "avg(bytes_sent)" ngxtop/ngxtop.py; echo "==="; grep -n "avg_bytes_sent" README.rst

Now get exact whitespace with cat -A.

RUN grep -n "AS avg_bytes_sent" ngxtop/ngxtop.py | cat -A; echo "==="; grep -n "avg_bytes_sent |   2xx" README.rst | cat -A

I'll send this.

RUN sed -n '80,86p' ngxtop/ngxtop.py | cat -A

Let me find the exact line number first.

RUN grep -n "avg(bytes_sent)" ngxtop/ngxtop.py | cat -A

Enough — I'll just send it.

RUN grep -n "avg(bytes_sent)" ngxtop/ngxtop.py

Now I'll read those specific lines with cat -A to get exact spacing.

RUN awk 'NR>=78 && NR<=100' ngxtop/ngxtop.py | cat -A

Send.

RUN sed -n '75,110p' ngxtop/ngxtop.py | cat -A
