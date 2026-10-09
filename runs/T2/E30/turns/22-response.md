The file is too large to reliably rewrite in one block. Let me use a different, robust approach: since RUN commands must be single-line, I'll apply edits via single-line `sed`/`python -c` commands (each a complete one-liner without heredocs or embedded newlines).

First, let me confirm current state.

RUN grep -c output-format ngxtop/ngxtop.py

Let me check.

Now let me apply edit 1 (docstring option) with a single-line python command using `re.sub` with `\n` escapes.

RUN .venv/bin/python -c "import re,io; p='ngxtop/ngxtop.py'; s=open(p).read(); s=s.replace('    -o <var>, --order-by <var>  order of output for default query [default: count]\n','    -o <var>, --order-by <var>  order of output for default query [default: count]\n    --output-format <fmt>  output format for default report: table or json [default: table]\n',1); open(p,'w').write(s)"

Let me verify.

RUN grep -n "output-format" ngxtop/ngxtop.py

Let me check.

Now edit 2: replace the `report` method with the expanded set. I'll do this via python with a marker-based substring replacement, using explicit `\n` in the string.

RUN .venv/bin/python -c "p='ngxtop/ngxtop.py'; s=open(p).read(); a=s.index('    def report(self):'); b=s.index('    def init_db(self):'); new='    def status_line(self):\n        count = self.count()\n        duration = time.time() - self.begin\n        status = \'running for %.0f seconds, %d records processed: %.2f req/sec\'\n        return status % (duration, count, count / duration)\n\n    def _report_data(self):\n        results = []\n        with closing(self.conn.cursor()) as cursor:\n            for query in self.report_queries:\n                label = \'\'\n                if isinstance(query, tuple):\n                    label, query = query\n                cursor.execute(query)\n                columns = [d[0] for d in cursor.description]\n                rows = cursor.fetchall()\n                results.append((label, columns, rows))\n        return results\n\n    def report(self):\n        if not self.begin:\n            return \'\'\n        output = [self.status_line()]\n        for label, columns, rows in self._report_data():\n            result = tabulate.tabulate(rows, headers=columns, tablefmt=\'orgtbl\', floatfmt=\'.3f\')\n            output.append(\'%s\\n%s\' % (label, result))\n        return \'\\n\\n\'.join(output)\n\n    def report_json(self):\n        if not self.begin:\n            return \'{}\'\n        data = self._report_data()\n        summary = {}\n        if len(data) > 0:\n            _, columns, rows = data[0]\n            if rows:\n                summary = dict(zip(columns, rows[0]))\n        detailed = []\n        if len(data) > 1:\n            _, columns, rows = data[1]\n            for row in rows:\n                detailed.append(dict(zip(columns, row)))\n        return json.dumps({\'summary\': summary, \'detailed\': detailed})\n\n'; s=s[:a]+new+s[b:]; open(p,'w').write(s)"

Let me verify.

RUN grep -n "def status_line\|def _report_data\|def report_json\|def report(" ngxtop/ngxtop.py

Let me check.

Now edit 3: process_log.

RUN .venv/bin/python -c "p='ngxtop/ngxtop.py'; s=open(p).read(); old='    processor.process(records)\n    print(processor.report())  # this will only run when start in --no-follow mode'; new='    processor.process(records)\n    # this will only run when start in --no-follow mode\n    output_format = arguments.get(\'--output-format\', \'table\')\n    if output_format == \'json\':\n        sys.stderr.write(processor.status_line() + \'\\n\')\n        print(processor.report_json())\n    else:\n        print(processor.report())'; assert old in s, 'not found'; s=s.replace(old,new,1); open(p,'w').write(s)"

Let me verify.

RUN grep -n "output_format\|report_json\|status_line" ngxtop/ngxtop.py

Let me check.

Now edit 4: main() validation.

RUN .venv/bin/python -c "p='ngxtop/ngxtop.py'; s=open(p).read(); old=\"    args = docopt(__doc__, version='xstat 0.1')\"; new=old+chr(10)+chr(10)+'    output_format = args.get('+chr(39)+'--output-format'+chr(39)+', '+chr(39)+'table'+chr(39)+')'+chr(10)+'    if output_format not in ('+chr(39)+'table'+chr(39)+', '+chr(39)+'json'+chr(39)+'):'+chr(10)+'        error_exit('+chr(39)+'invalid --output-format value: %s (expected: table or json)'+chr(39)+' % output_format)'; assert old in s, 'docopt line not found'; s=s.replace(old,new,1); open(p,'w').write(s)"

Let me verify.

RUN grep -n "output_format not in" ngxtop/ngxtop.py

Let me check.

Now let me run the acceptance tests. First the illegal value.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml; echo "rc=$?"

Let me run.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml 2>&1; echo "rc=$?"

Let me run illegal case.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml > /tmp/y.out 2>/tmp/y.err; echo "rc=$?"; echo "OUT:"; cat /tmp/y.out; echo "ERR:"; cat /tmp/y.err

Let me run this.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml > /tmp/y.out 2>/tmp/y.err; echo "rc=$?"; echo "OUT:"; cat /tmp/y.out; echo "ERR:"; cat /tmp/y.err

Let me run.

Now the json example.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json > /tmp/j.out 2>/tmp/j.err; echo "rc=$?"; echo "OUT:"; cat /tmp/j.out; echo "ERR:"; cat /tmp/j.err

Let me run this.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>/dev/null

Let me run.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>&1

Let me run.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>&1 | cat

Let me try.
