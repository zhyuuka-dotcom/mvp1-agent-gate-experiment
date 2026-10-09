Everything works:
- Default/explicit table output identical (only the timing value differs, which is expected).
- `-g` single and multi-column grouping works in both table and JSON modes; JSON keys follow group columns.
- stdout is exactly one valid JSON document.
- Invalid value → exit code 2, single error line on stderr, empty stdout.
- All 28 existing tests pass.

One edge case worth confirming: the `detailed` key detection when a group-by column could shadow the "summary"/"detailed" labels is a non-issue since labels come from the fixed DEFAULT_QUERIES. Also let me confirm stdin mode and `-g` with the `-o` order-by combined format string case still works fine (the task's bullet 8 mentions "直传格式串组合").

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">echo "=== stdin + json ==="; cat repro/combined.log | .venv/bin/python -m ngxtop.ngxtop -f combined --no-follow --output-format json 2>/tmp/serr; echo "stderr:"; grep running /tmp/serr
echo "=== format string direct + -g + json ==="; .venv/bin/python -m ngxtop.ngxtop -f '$remote_addr - - [$time_local] "$request" $status $bytes_sent' -l repro/combined.log --no-follow -g remote_addr --output-format json 2>/dev/null</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
