My full-file writes keep getting truncated. Let me switch strategy: use RUN with a python script passed via a single `-c` argument (base64 or simple) to patch precisely. I'll avoid heredocs. I'll do the edits step by step with small python -c commands using double quotes carefully, or better, use `sed`.

Actually the simplest robust approach: use `sed` to insert lines. But multiline insertion of the class is hard with sed. Instead, I can create the Median class as a small separate module file (new file, allowed if in whitelist!). My whitelist includes tests/test_median.py, ngxtop/ngxtop.py, README.rst. A separate module isn't whitelisted. 

Alternative: keep Median inline but insert it via python using `-c` with the script encoded to avoid quoting issues. Let me use base64.

Plan:
1. Write the patch python script content... but writing a file isn't whitelisted. I can pass base64 string directly to `python -c`:

RUN echo "<b64>" | base64 -d | .venv/bin/python

Wait, python reading from stdin: `.venv/bin/python -` reads script from stdin. So:
`echo '<b64>' | base64 -d | .venv/bin/python -`

That avoids heredoc. Let me base64-encode the patch script. I'll produce the base64 manually? Hard. Instead, generate base64 in one RUN from an echo of the script... circular.

Better approach: do the edits with a sequence of small, robust RUN commands using python `-c` with single quotes wrapping, since the script contains double quotes mostly. Let me write the class insertion using a python -c that builds the class string from a triple-quoted string... quoting nightmare inside -c with single quotes.

Cleanest: use ed? Not available maybe.

Alternative robust approach: Since only 3 small edits, I can do them with `sed`:
- Edit A: after the line `from .utils import error_exit`, insert a marker line, then later replace marker? Still multiline.

Let me try: use `python -c` where the script is provided via an environment variable containing newlines. I can set env var with `$'...'`? Complex.

Simplest reliable: multiple WRITE attempts were failing due to length/complexity in my message. Let me instead make the edits minimal by NOT adding a big class — I can define median using a compact lambda-free tick class in few lines. But still multiline.

Actually, maybe the WRITE failure was because my message got cut off by length. Let me try a much shorter full-file write? The file is ~460 lines; that's a lot.

Better: patch with python -c using a compact script that reads/writes. Let me write the class using "\n".join of a list, all on one line, with the whole -c argument quoted in double quotes and internal strings in single quotes. The class text contains no double quotes if I use single quotes for docstrings? Docstrings need quotes; I'll use single quotes inside. But then shell double-quote wrapping keeps single quotes literal — fine. And `\n` inside python string literal in double-quoted shell: shell passes `\n` through (backslash-n) to python, python interprets as newline. Good.

Let me construct:

.venv/bin/python -c "p='ngxtop/ngxtop.py'; s=open(p).read(); cls=['class Median(object):', '    ...', ...]; ..."

The class body lines need leading spaces; fine. And I use chr(10).join(cls). Let me build the list with single-quoted elements, avoiding single quotes inside. Docstring: use no triple quotes; skip docstring to keep it simple, use comment lines instead? Comments are fine. But the class needs indentation.

Let me write the script carefully as one shell argument (double quotes). Internal uses single quotes only. Watch: contains `%`? no. Contains backticks? no. Contains `$`? no. Contains `!`? no. Good for double-quoting (history expansion only in interactive; non-interactive bash fine).

Script:
import io
p='ngxtop/ngxtop.py'
s=open(p).read()
nl=chr(10)
cls=nl.join([
'class Median(object):',
'    """SQLite aggregate computing the median, ignoring NULLs."""',
'',
'    def __init__(self):',
'        self.values = []',
'',
'    def step(self, value):',
'        if value is not None:',
'            self.values.append(value)',
'',
'    def finalize(self):',
'        if not self.values:',
'            return None',
'        values = sorted(self.values)',
'        n = len(values)',
'        mid = n // 2',
'        if n % 2 == 1:',
'            return values[mid]',
'        return (values[mid - 1] + values[mid]) / 2.0',
''])
anchor='from .utils import error_exit'+nl
s=s.replace(anchor, anchor+nl+cls+nl, 1)
old='       avg(bytes_sent)                             AS avg_bytes_sent,'+nl
new=old+'       median(bytes_sent)                          AS median_bytes_sent,'+nl
s=s.replace(old,new,2)
conn="        self.conn = sqlite3.connect(':memory:')"+nl
s=s.replace(conn, conn+"        self.conn.create_aggregate('median', 1, Median)"+nl, 1)
open(p,'w').write(s)
print('ok', s.count('Median'))

The docstring uses triple double-quotes inside a shell double-quoted string — that WILL terminate shell quoting. Avoid double quotes. Use single-quote docstring? Triple single quotes inside single... no, shell arg is double-quoted, so single quotes are literal and fine: use `'''...'''`. That has single quotes only — fine inside double quotes.

Let me finalize and send as one RUN. The semicolons/newlines: python -c can take newlines inside the double-quoted arg since shell passes them. Good.

Send.Patch via a single `python -c` argument (avoids heredoc/full-file write).

RUN .venv/bin/python -c "
nl = chr(10)
p = 'ngxtop/ngxtop.py'
s = open(p).read()
cls = nl.join([
'class Median(object):',
'    ' + chr(39)*3 + 'SQLite aggregate computing the median, ignoring NULLs.' + chr(39)*3,
'',
'    def __init__(self):',
'        self.values = []',
'',
'    def step(self, value):',
'        if value is not None:',
'            self.values.append(value)',
'',
'    def finalize(self):',
'        if not self.values:',
'            return None',
'        values = sorted(self.values)',
'        n = len(values)',
'        mid = n // 2',
'        if n % 2 == 1:',
'            return values[mid]',
'        return (values[mid - 1] + values[mid]) / 2.0',
''])
anchor = 'from .utils import error_exit' + nl
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + nl + cls + nl, 1)
old = '       avg(bytes_sent)                             AS avg_bytes_sent,' + nl
assert s.count(old) == 2
new = old + '       median(bytes_sent)                          AS median_bytes_sent,' + nl
s = s.replace(old, new, 2)
conn = '        self.conn = sqlite3.connect(' + chr(39) + ':memory:' + chr(39) + ')' + nl
assert s.count(conn) == 1
s = s.replace(conn, conn + '        self.conn.create_aggregate(' + chr(39) + 'median' + chr(39) + ', 1, Median)' + nl, 1)
open(p, 'w').write(s)
print('ok', s.count('Median'))
"

Send.
