File is unchanged. Now I'll do targeted edits with RUN (python/sed) instead of a full overwrite, to reduce risk. But RUN editing files isn't gated, and it's allowed. However, cleanest is to use WRITE with the complete content. The file is long; risk of truncation repeats. I'll instead apply three precise patches using python via RUN.

Patch 1: Insert Median class after the `from .utils import error_exit` line.
Patch 2: Add median column after each `AS avg_bytes_sent,` line.
Patch 3: Register aggregate in init_db (add a line after `self.conn = sqlite3.connect(':memory:')`).

Let me do it with a python script written via a here-doc? The RUN command with heredoc may work. Let me use sed-like python -c with careful quoting. Simpler: use `python - <<'EOF'` heredoc.

RUN .venv/bin/python - <<'PYEOF'
import re
p='ngxtop/ngxtop.py'
s=open(p).read()

median_cls = '''class Median(object):
    """SQLite aggregate function computing the median of a column of values.

    Registered as ``median()`` on the sqlite connection so that the default
    report can show the median of ``bytes_sent`` next to its average. NULL
    values (e.g. records without ``bytes_sent``) are ignored; when no value
    is passed at all the result is NULL.
    """

    def __init__(self):
        self.values = []

    def step(self, value):
        if value is not None:
            self.values.append(value)

    def finalize(self):
        if not self.values:
            return None
        values = sorted(self.values)
        n = len(values)
        mid = n // 2
        if n % 2 == 1:
            return values[mid]
        return (values[mid - 1] + values[mid]) / 2.0


'''

anchor='from .utils import error_exit\n'
assert s.count(anchor)==1
s=s.replace(anchor, anchor+'\n\n'+median_cls, 1)

old_avg='       avg(bytes_sent)                             AS avg_bytes_sent,\n'
new_avg=old_avg+'       median(bytes_sent)                          AS median_bytes_sent,\n'
assert s.count(old_avg)==2, s.count(old_avg)
s=s.replace(old_avg, new_avg, 2)

conn='        self.conn = sqlite3.connect(\':memory:\')\n'
assert s.count(conn)==1
s=s.replace(conn, conn+'        self.conn.create_aggregate(\'median\', 1, Median)\n', 1)

open(p,'w').write(s)
print('ok')
PYEOF

Let me send this.File unchanged. I'll apply three precise patches via a python script (RUN), which avoids a risky full overwrite.

RUN .venv/bin/python - <<'PYEOF'
p='ngxtop/ngxtop.py'
s=open(p).read()

median_cls = '''class Median(object):
    """SQLite aggregate function computing the median of a column of values.

    Registered as ``median()`` on the sqlite connection so that the default
    report can show the median of ``bytes_sent`` next to its average. NULL
    values (e.g. records without ``bytes_sent``) are ignored; when no value
    is passed at all the result is NULL.
    """

    def __init__(self):
        self.values = []

    def step(self, value):
        if value is not None:
            self.values.append(value)

    def finalize(self):
        if not self.values:
            return None
        values = sorted(self.values)
        n = len(values)
        mid = n // 2
        if n % 2 == 1:
            return values[mid]
        return (values[mid - 1] + values[mid]) / 2.0


'''

anchor='from .utils import error_exit\n'
assert s.count(anchor)==1
s=s.replace(anchor, anchor+'\n\n'+median_cls, 1)

old_avg='       avg(bytes_sent)                             AS avg_bytes_sent,\n'
new_avg=old_avg+'       median(bytes_sent)                          AS median_bytes_sent,\n'
assert s.count(old_avg)==2, s.count(old_avg)
s=s.replace(old_avg, new_avg, 2)

conn="        self.conn = sqlite3.connect(':memory:')\n"
assert s.count(conn)==1
s=s.replace(conn, conn+"        self.conn.create_aggregate('median', 1, Median)\n", 1)

open(p,'w').write(s)
print('patched ok')
PYEOF

Send.
