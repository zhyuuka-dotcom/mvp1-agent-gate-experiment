Now I have a clear picture. Let me design the implementation.

**Plan:**
1. Add `--output-format <fmt>` to docopt usage (default `table`).
2. `SQLProcessor.report()` keeps table behavior (tests rely on it). Add a `report_data()` method returning structured data (status line + summary dict + detailed list).
3. In `process_log`, for `--no-follow` mode: if output-format is `json`, print status to stderr and JSON to stdout; else keep current behavior.
4. Validate `--output-format` value.

Let me implement. First, add the docopt option.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="READ">
<｜｜DSML｜｜ parameter name="path">ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
