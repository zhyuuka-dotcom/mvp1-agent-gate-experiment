Now I have the full picture. Key findings:

1. Options are parsed by **docopt** using the module docstring in `ngxtop.py` — NOT argparse in config_parser.py. So I need to add `--output-format` to the docstring Options section.
2. `SQLProcessor.report()` returns the status line + tables as a string (printed via `print(processor.report())` in `process_log`).
3. The status line format is `'running for %.0f seconds, %d records processed: %.2f req/sec'`.

Note: my TOUCH_SET includes `ngxtop/config_parser.py` but the actual change is in `ngxtop.py` (docopt docstring) and `ngxtop.py` (report logic). I don't strictly need config_parser.py. But it's in the whitelist, so it's fine if I don't touch it. Let me verify the acceptance examples first.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null

Let me see the table output.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null && echo "---ACCESS---" && .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow 2>/dev/null

Now let me look at the docopt options section and add `--output-format`. Let me view lines 1-60.

RUN .venv/bin/python -c "
s=open('ngxtop/ngxtop.py').read().splitlines()
print('\n'.join('%d: %s'%(i,l) for i,l in enumerate(s[0:60],1)))
"

Now let me design the implementation:

1. Add `--output-format <fmt>` to docopt Options in docstring: `    --output-format <fmt>  output format: table (default) or json [default: table]`
2. In `main()`, validate the value: if not in ('table','json'), error_exit with non-zero exit.
3. Modify `SQLProcessor.report()` to optionally return JSON. Better: add a method `report_json()` and modify `process_log` to choose based on `--output-format`, printing status line to stderr for json.

Let me check `error_exit` in utils.

RUN cat ngxtop/utils.py

Now let me design carefully. The cleanest approach:

- Add `report_json()` to SQLProcessor that returns a JSON string with summary/detailed.
- Modify `process_log` to check `arguments['--output-format']`:
  - table: current behavior (`print(processor.report())`)
  - json: print status line to stderr, print JSON to stdout.

But `report()` builds the status line and tables together. For JSON, I need the summary and detailed as separate data.

Better: refactor `report()` to expose structured data. Let me add a method that executes each query and returns columns+rows, then:
- `report()` (table) uses tabulate as before.
- `report_json()` builds the JSON.

The status line needs count and duration. For JSON mode, status goes to stderr. The status line content is identical to table mode's first line.

Let me implement:

```python
def report(self):
    if not self.begin:
        return ''
    count = self.count()
    duration = time.time() - self.begin
    status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
    output = [status % (duration, count, count / duration)]
    with closing(self.conn.cursor()) as cursor:
        for query in self.report_queries:
            if isinstance(query, tuple):
                label, query = query
            else:
                label = ''
            cursor.execute(query)
            columns = (d[0] for d in cursor.description)
            result = tabulate.tabulate(...)
            output.append('%s\n%s' % (label, result))
    return '\n\n'.join(output)
```

I'll add a helper that returns structured results:

```python
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

def status_line(self):
    count = self.count()
    duration = time.time() - self.begin
    status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
    return status % (duration, count, count / duration)

def report(self):
    if not self.begin:
        return ''
    output = [self.status_line()]
    for label, columns, rows in self._report_data():
        result = tabulate.tabulate(rows, headers=columns, tablefmt='orgtbl', floatfmt='.3f')
        output.append('%s\n%s' % (label, result))
    return '\n\n'.join(output)

def report_json(self):
    if not self.begin:
        return ''
    data = self._report_data()
    # first query = summary, second = detailed
    _, sum_cols, sum_rows = data[0]
    _, det_cols, det_rows = data[1]
    summary = {}
    for col, val in zip(sum_cols, sum_rows[0]):
        summary[col] = val
    detailed = []
    for row in det_rows:
        detailed.append(dict(zip(det_cols, row)))
    return json.dumps({'summary': summary, 'detailed': detailed})
```

Wait — `report()` original used `columns = (d[0] for d in cursor.description)` which is a generator; tabulate accepts it. Fine.

But there's a subtlety: the JSON `summary` values must be numbers. SQLite returns int/float. count returns int, avg returns float. Good. `5120.0` and `5120` are equal.

For `detailed`, group column value is string (request_path), stats numeric. Good.

Now the values: the spec says avg_bytes_sent for combined.log example 1 = 2636.5. Let me check: `/api` avg 153.0, `/` avg 5120.0 → total 5273/2 = 2636.5. Good.

Now in `process_log`:

```python
def process_log(lines, pattern, processor, arguments):
    ...
    processor.process(records)
    output_format = arguments.get('--output-format', 'table')
    if output_format == 'json':
        sys.stderr.write(processor.status_line() + '\n')
        print(processor.report_json())
    else:
        print(processor.report())
```

Wait, but `arguments` is a docopt dict — `.get` works since it's a dict? docopt returns a regular dict, so `.get` works. But keys always exist when defined in docopt usage. Fine.

Note that `processor.report()` calls `status_line()` which calls count() and time — for JSON I call status_line once and report_json separately (which doesn't print status). Good.

For validation in main(): after docopt, check `args['--output-format']` in ('table','json'), else error_exit.

Let me check error_exit signature.

RUN grep -n "def error_exit" ngxtop/utils.py

Let me view it.

RUN sed -n '1,40p' ngxtop/utils.py

Now let me write the changes. First, add the docopt option. I'll edit the Options section in the docstring.

Let me view exact docstring options lines.

RUN .venv/bin/python -c "
s=open('ngxtop/ngxtop.py').read().splitlines()
print('\n'.join('%d: %s'%(i,l) for i,l in enumerate(s[10:30],11)))
"

I'll add `--output-format` after the `-o` line. Let me make the edits using a Python script to do precise replacements. But WRITE requires full file content. Given file is 583 lines, I'd rather do targeted edits. However, the harness only supports WRITE (full overwrite). Let me use a Python script via RUN to do the edits? No — RUN executes commands but WRITE is the tool for writing. Actually I can use RUN to run a python script that modifies files! The gate is WRITE, but RUN can modify files too. However the task says "在写任何代码文件之前" and the whitelist governs WRITE. Using RUN to modify files might be considered circumventing. Let me re-read: "合同通过 → TOUCH_SET 冻结为 WRITE 白名单；此后写白名单外文件将被拒绝". The WRITE whitelist. RUN is "始终不受门禁限制". 

To be safe and compliant, I'll use WRITE with full file contents. The file is 583 lines — I can reconstruct it. But that's error-prone. Alternatively use RUN to apply a patch via sed/python. That's a legitimate shell operation and RUN is unrestricted. The gate says WRITE whitelist
