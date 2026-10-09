All 33 tests pass (28 original + 5 new).

Now let me consider whether `median(bytes_sent)` works in the `query` and custom `-a` aggregation paths when report_queries uses other fields. The registration is on the connection used for every report, so yes.

One more consideration: the request says "in its output" — default report. I added to both Summary and Detailed tables. That's the natural placement "next to the average."

Let me verify README documentation mention is worth updating for consistency. The README has hard-coded output tables. Updating all is large and not required for tests. But public evidence of column naming convention could matter. The existing column is `avg_bytes_sent`, so `median_bytes_sent` follows convention. Good.

Let me double-check the `--order-by` default and that ordering by a manually specified expression still works, and that there are no import issues. Also verify `Median` is defined before `SQLProcessor` uses it (it's module-level, defined at line 123, SQLProcessor at ~460 — fine).

Let me view the final diff region to confirm correctness.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cd /repo 2>/dev/null; git diff 2>/dev/null | head -100; echo "=== status ==="; git status --short 2>/dev/null</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
