The harness truncated my long command. I need to keep commands SHORT. 

New strategy: Build the replacement block in `/tmp/newblock.txt` incrementally with several short `printf` commands that APPEND (`>>`), each short. Then run a short patch script.

Let me start fresh: create the file with the first line.

RUN printf '%s\n' '    def status_line(self):' > /tmp/nb.txt

Then append each line with short commands.

RUN printf '%s\n' '        count = self.count()' >> /tmp/nb.txt

RUN printf '%s\n' '        duration = time.time() - self.begin' >> /tmp/nb.txt

RUN printf '%s\n' "        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'" >> /tmp/nb.txt

RUN printf '%s\n' '        return status % (duration, count, count / duration)' >> /tmp/nb.txt

RUN printf '\n' >> /tmp/nb.txt

RUN printf '%s\n' '    def _report_data(self):' >> /tmp/nb.txt

RUN printf '%s\n' '        results = []' >> /tmp/nb.txt

RUN printf '%s\n' '        with closing(self.conn.cursor()) as cursor:' >> /tmp/nb.txt

RUN printf '%s\n' '            for query in self.report_queries:' >> /tmp/nb.txt

RUN printf '%s\n' "                label = ''" >> /tmp/nb.txt

RUN printf '%s\n' '                if isinstance(query, tuple):' >> /tmp/nb.txt

RUN printf '%s\n' '                    label, query = query' >> /tmp/nb.txt

RUN printf '%s\n' '                cursor.execute(query)' >> /tmp/nb.txt

RUN printf '%s\n' '                columns = [d[0] for d in cursor.description]' >> /tmp/nb.txt

RUN printf '%s\n' '                rows = cursor.fetchall()' >> /tmp/nb.txt

RUN printf '%s\n' '                results.append((label, columns, rows))' >> /tmp/nb.txt

RUN printf '%s\n' '        return results' >> /tmp/nb.txt

RUN printf '\n' >> /tmp/nb.txt

RUN printf '%s\n' '    def report(self):' >> /tmp/nb.txt

RUN printf '%s\n' '        if not self.begin:' >> /tmp/nb.txt

RUN printf '%s\n' "            return ''" >> /tmp/nb.txt

RUN printf '%s\n' '        output = [self.status_line()]' >> /tmp/nb.txt

RUN printf '%s\n' '        for label, columns, rows in self._report_data():' >> /tmp/nb.txt

RUN printf '%s\n' "            result = tabulate.tabulate(rows, headers=columns, tablefmt='orgtbl', floatfmt='.3f')" >> /tmp/nb.txt

RUN printf '%s\n' "            output.append('%s\n%s' % (label, result))" >> /tmp/nb.txt

RUN printf '%s\n' "        return '\n\n'.join(output)" >> /tmp/nb.txt

RUN printf '\n' >> /tmp/nb.txt

RUN printf '%s\n' '    def report_json(self):' >> /tmp/nb.txt

RUN printf '%s\n' '        if not self.begin:' >> /tmp/nb.txt

RUN printf '%s\n' "            return '{}'" >> /tmp/nb.txt

RUN printf '%s\n' '        data = self._report_data()' >> /tmp/nb.txt

RUN printf '%s\n' '        summary = {}' >> /tmp/nb.txt

RUN printf '%s\n' '        if len(data) > 0:' >> /tmp/nb.txt

RUN printf '%s\n' '            _, columns, rows = data[0]' >> /tmp/nb.txt

RUN printf '%s\n' '            if rows:' >> /tmp/nb.txt

RUN printf '%s\n' '                summary = dict(zip(columns, rows[0]))' >> /tmp/nb.txt

RUN printf '%s\n' '        detailed = []' >> /tmp/nb.txt

RUN printf '%s\n' '        if len(data) > 1:' >> /tmp/nb.txt

RUN printf '%s\n' '            _, columns, rows = data[1]' >> /tmp/nb.txt

RUN printf '%s\n' '            for row in rows:' >> /tmp/nb.txt

RUN printf '%s\n' '                detailed.append(dict(zip(columns, row)))' >> /tmp/nb.txt

RUN printf '%s\n' "        return json.dumps({'summary': summary, 'detailed': detailed})" >> /tmp/nb.txt

RUN printf '\n' >> /tmp/nb.txt

Let me verify the block so far.

RUN cat -A /tmp/nb.txt

Let me view it.

RUN wc -l /tmp/nb.txt

Let me check line count.

Now the patch script:

RUN printf '%s\n' "p='ngxtop/ngxtop.py'" "s=open(p).read()" "a=s.index('    def report(self):')" "b=s.index('    def init_db(self):')" "new=open('/tmp/nb.txt').read()" "s=s[:a]+new+s[b:]" "open(p,'w').write(s)" "print('OK', 'report_json' in s)" > /tmp/patch.py; cat /tmp/patch.py

Then run it.

RUN python3 /tmp/patch.py

Let me run the patch.

Let me first inspect /tmp/nb.txt content.

RUN cat /tmp/nb.txt

Now run patch.

RUN python3 /tmp/patch.py

Let me run and verify.

RUN grep -n "def report_json\|def status_line\|def _report_data" ngxtop/ngxtop.py

Let me check.

I need to check whether the printf appends worked (each is a separate RUN, must persist). Let me verify.

RUN wc -l /tmp/nb.txt

Let me check.

Waiting for outputs. Let me proceed step by step, checking as I go.
