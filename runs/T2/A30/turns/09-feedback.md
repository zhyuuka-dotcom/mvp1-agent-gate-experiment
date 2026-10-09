$ cd /tmp/t2a30/repo 2>/dev/null || cd .; python - <<'EOF'
import re
p = 'ngxtop/ngxtop.py'
s = open(p).read()

# 1. Add option to usage
old = "    -n <number>, --limit <number>  limit the number of records included in report for top command [default: 10]\n"
new = old + "    --output-format <fmt>  output format: table or json [default: table]\n"
assert old in s
s = s.replace(old, new, 1)

# 2. Add report_data method and refactor report
old_report = '''    def report(self):
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
                result = tabulate.tabulate(cursor.fetchall(), headers=columns, tablefmt='orgtbl', floatfmt='.3f')
                output.append('%s\\n%s' % (label, result))
        return '\\n\\n'.join(output)
'''
new_report = '''    def status_line(self):
        count = self.count()
        duration = time.time() - self.begin
        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
        return status % (duration, count, count / duration)

    def report_data(self):
        """Return structured report data: list of (label, columns, rows)."""
        if not self.begin:
            return []
        sections = []
        with closing(self.conn.cursor()) as cursor:
            for query in self.report_queries:
                if isinstance(query, tuple):
                    label, query = query
                else:
                    label = ''
                cursor.execute(query)
                columns = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                sections.append((label, columns, rows))
        return sections

    def report(self):
        if not self.begin:
            return ''
        output = [self.status_line()]
        for label, columns, rows in self.report_data():
            result = tabulate.tabulate(rows, headers=columns, tablefmt='orgtbl', floatfmt='.3f')
            output.append('%s\\n%s' % (label, result))
        return '\\n\\n'.join(output)

    def report_json(self):
        """Return a JSON string with summary and detailed sections."""
        data = {'summary': {}, 'detailed': []}
        for label, columns, rows in self.report_data():
            label_text = (label or '').strip().rstrip(':').lower()
            if not rows:
                continue
            if label_text.startswith('summary'):
                data['summary'] = dict(zip(columns, rows[0]))
            elif label_text.startswith('detailed'):
                data['detailed'] = [dict(zip(columns, row)) for row in rows]
        return json.dumps(data)
'''
assert old_report in s
s = s.replace(old_report, new_report, 1)

# 3. Update process_log to handle output format
old_pl = '''    processor.process(records)
    print(processor.report())  # this will only run when start in --no-follow mode
'''
new_pl = '''    processor.process(records)
    output_format = arguments.get('--output-format', 'table')
    if output_format == 'json':
        sys.stderr.write(processor.status_line() + '\\n')
        print(processor.report_json())
    else:
        print(processor.report())  # this will only run when start in --no-follow mode
'''
assert old_pl in s
s = s.replace(old_pl, new_pl, 1)

# 4. Validate output-format in process() before processing
old_proc = '''    source = build_source(access_log, arguments)
    pattern = build_pattern(log_format)'''
new_proc = '''    output_format = arguments.get('--output-format', 'table')
    if output_format not in ('table', 'json'):
        error_exit('invalid output format "%s" (expected: table, json)' % output_format, status=2)

    source = build_source(access_log, arguments)
    pattern = build_pattern(log_format)'''
assert old_proc in s
s = s.replace(old_proc, new_proc, 1)

open(p, 'w').write(s)
print("done")
EOF
done

[exit code: 0]