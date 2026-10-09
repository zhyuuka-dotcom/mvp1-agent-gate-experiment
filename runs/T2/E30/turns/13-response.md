Let me use WRITE with full file content. First, let me get the exact full content of ngxtop.py to edit precisely. I'll write the whole file. Let me read it once more fully, then produce the modified version.

Actually, a cleaner approach: I'll use RUN with a Python script to perform targeted replacements, then WRITE nothing (RUN isn't gated). But to respect the spirit, let me reconsider — the gate explicitly says RUN is unrestricted. Using a script to edit is fine. However the cleanest, most auditable approach given a 583-line file is targeted sed/python edits via RUN.

Let me do targeted edits with Python via a heredoc script file. But I can't WRITE a script outside TOUCH_SET. I can use RUN with inline python carefully avoiding quote issues.

Let me first make the three edits. Edit 1: docstring — add `--output-format` option line.

Let me check the exact line for the `-o` option.

RUN grep -n "order-by\|output-format\|having clause" ngxtop/ngxtop.py

Let me view the options region.

RUN sed -n '18,26p' ngxtop/ngxtop.py

I'll add the option after the `-o` line (line 23). Let me identify exact text.

RUN sed -n '23p' ngxtop/ngxtop.py | cat -A

Now, let me perform edits via a python script using a heredoc that doesn't conflict. I'll use single-quoted heredoc delimiter and write in the script.

Actually let me just do the edits with `python3 - <<'PY'` reading/writing the file. RUN is unrestricted.

Let me be careful. I'll do edit 1.

RUN cat ngxtop/ngxtop.py | head -30 | tail -13

Let me get exact bytes of the options block.

RUN sed -n '12,26p' ngxtop/ngxtop.py

Now edit: insert after line 23 (`    -o <var>, --order-by <var>  order of output for default query [default: count]`) a new line.

Let me do the docstring edit with python.

RUN .venv/bin/python - <<'PY'
import io
p = 'ngxtop/ngxtop.py'
s = open(p, encoding='utf-8').read()
old = "    -o <var>, --order-by <var>  order of output for default query [default: count]\n"
assert old in s, "docopt option line not found"
new = old + "    --output-format <fmt>  output format: table (default) or json [default: table]\n"
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(s)
print("docstring updated")
PY

Now let me verify.

RUN sed -n '20,28p' ngxtop/ngxtop.py

Now edit 2: add JSON methods to SQLProcessor. Let me view the report method again.

RUN grep -n "def report\|def count\|def init_db\|def process" ngxtop/ngxtop.py

Let me view the report method lines.

RUN sed -n '432,455p' ngxtop/ngxtop.py

Let me get the exact block.

RUN sed -n '430,458p' ngxtop/ngxtop.py | cat -n

Let me view precisely.

RUN .venv/bin/python - <<'PY'
s = open('ngxtop/ngxtop.py').read().splitlines()
for i,l in enumerate(s,1):
    if 'def report' in l or 'def count' in l or 'status =' in l or 'return' in l and i>430 and i<460:
        pass
for i,l in enumerate(s[430:460],431):
    print(i, repr(l))
PY

Now let me do the report refactor. I'll replace the `report` method with an expanded version that includes `status_line`, `_report_data`, `report`, and `report_json`.

Let me get the exact current text.

RUN .venv/bin/python - <<'PY'
s = open('ngxtop/ngxtop.py').read()
import re
start = s.index('    def report(self):')
end = s.index('    def init_db(self):')
print(repr(s[start:end]))
PY

Now I'll replace that block.

RUN .venv/bin/python - <<'PY'
p = 'ngxtop/ngxtop.py'
s = open(p, encoding='utf-8').read()
start = s.index('    def report(self):')
end = s.index('    def init_db(self):')
new_block = '''    def status_line(self):
        count = self.count()
        duration = time.time() - self.begin
        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
        return status % (duration, count, count / duration)

    def _report_data(self):
        """Execute report queries and return list of (label, columns, rows)."""
        results = []
        with closing(self.conn.cursor()) as cursor:
            for query in self.report_queries:
                label = ''
                if isinstance(query, tuple):
                    label, query = query
                cursor.execute(query)
                columns = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                results.append((label, columns, rows))
        return results

    def report(self):
        if not self.begin:
            return ''
        output = [self.status_line()]
        for label, columns, rows in self._report_data():
            result = tabulate.tabulate(rows, headers=columns, tablefmt='orgtbl', floatfmt='.3f')
            output.append('%s\\n%s' % (label, result))
        return '\\n\\n'.join(output)

    def report_json(self):
        """Return report as a JSON document with 'summary' and 'detailed' keys."""
        if not self.begin:
            return '{}'
        data = self._report_data()
        summary = {}
        if len(data) > 0:
            _, columns, rows = data[0]
            if rows:
                summary = dict(zip(columns, rows[0]))
        detailed = []
        if len(data) > 1:
            _, columns, rows = data[1]
            for row in rows:
                detailed.append(dict(zip(columns, row)))
        return json.dumps({'summary': summary, 'detailed': detailed})

'''
s = s[:start] + new_block + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print("report block updated")
PY

Now let me verify.

RUN sed -n '430,485p' ngxtop/ngxtop.py

Now edit 3: modify `process_log` to handle output format. Let me view it.

RUN grep -n "def process_log" ngxtop/ngxtop.py

RUN sed -n '507,525p' ngxtop/ngxtop.py

Let me find exact.

RUN .venv/bin/python - <<'PY'
s = open('ngxtop/ngxtop.py').read()
i = s.index('def process_log')
print(repr(s[i:i+500]))
PY

Now replace `print(processor.report())  # this will only run when start in --no-follow mode` with format-aware code.

RUN .venv/bin/python - <<'PY'
p = 'ngxtop/ngxtop.py'
s = open(p, encoding='utf-8').read()
old = "    processor.process(records)\n    print(processor.report())  # this will only run when start in --no-follow mode"
assert old in s, "process_log tail not found"
new = """    processor.process(records)
    # this will only run when start in --no-follow mode
    output_format = arguments.get('--output-format', 'table')
    if output_format == 'json':
        sys.stderr.write(processor.status_line() + '\\n')
        print(processor.report_json())
    else:
        print(processor.report())"""
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(s)
print("process_log updated")
PY

Now edit 4: validate `--output-format` in main(). Let me view main.

RUN grep -n "def main" ngxtop/ngxtop.py && sed -n '575,600p' ngxtop/ngxtop.py

Let me view main.

RUN .venv/bin/python - <<'PY'
s = open('ngxtop/ngxtop.py').read()
i = s.index('def main():')
print(s[i:i+600])
PY

Now add validation. Let me replace the docopt line region.

RUN .venv/bin/python - <<'PY'
p = 'ngxtop/ngxtop.py'
s = open(p, encoding='utf-8').read()
old = "    args = docopt(__doc__, version='xstat 0.1')\n"
assert old in s
new = old + """
    output_format = args.get('--output-format', 'table')
    if output_format not in ('table', 'json'):
        error_exit('invalid --output-format value: %s (expected: table or
