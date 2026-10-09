Now patch `process_log`, `build_processor`, and `process()`.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cat > /tmp/patch3.py << 'PYEOF'
p = 'ngxtop/ngxtop.py'
s = open(p).read()

# --- build_processor: track default report and pass flag ---
old = """    else:
        report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]
        fields = DEFAULT_FIELDS.union(set([arguments['--group-by']]))
"""
new = """    else:
        report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]
        fields = DEFAULT_FIELDS.union(set([arguments['--group-by']]))
        is_default_report = True
"""
assert old in s, "build_processor else anchor missing"
s = s.replace(old, new, 1)

old = """def build_processor(arguments):
    fields = arguments['<var>']
    if arguments['print']:
"""
new = """def build_processor(arguments):
    fields = arguments['<var>']
    is_default_report = False
    if arguments['print']:
"""
assert old in s, "build_processor head anchor missing"
s = s.replace(old, new, 1)

old = """    processor = SQLProcessor(report_queries, processor_fields)
    return processor
"""
new = """    processor = SQLProcessor(report_queries, processor_fields, is_default_report=is_default_report)
    return processor
"""
assert old in s
s = s.replace(old, new, 1)

# --- process_log: render based on output format ---
old = """    processor.process(records)
    print(processor.report())  # this will only run when start in --no-follow mode
"""
new = """    processor.process(records)
    # this will only run when start in --no-follow mode
    output_format = arguments['--output-format']
    if output_format == 'json' and processor.is_default_report:
        # Status line goes to stderr, the JSON document to stdout.
        sys.stderr.write(processor.status_line() + '\\n')
        print(json.dumps(processor.json_report()))
    else:
        print(processor.report())
"""
assert old in s, "process_log anchor missing"
s = s.replace(old, new, 1)

# --- process(): validate output format early ---
old = """def process(arguments):
    access_log = arguments['--access-log']
    log_format = arguments['--log-format']
"""
new = """def process(arguments):
    output_format = arguments['--output-format']
    if output_format not in VALID_OUTPUT_FORMATS:
        error_exit('invalid output format "%s", expected one of: %s'
                   % (output_format, ', '.join(VALID_OUTPUT_FORMATS)))

    access_log = arguments['--access-log']
    log_format = arguments['--log-format']
"""
assert old in s, "process() anchor missing"
s = s.replace(old, new, 1)

open(p,'w').write(s)
print("patched process_log/build_processor/process")
PYEOF
.venv/bin/python /tmp/patch3.py && grep -n "is_default_report\|output_format\|output-format\|error_exit" ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ calls>
