JSON and table paths agree (both 0 records, since that format genuinely doesn't match combined.log's lines — a data mismatch in my synthetic test, not a code issue). JSON is valid, `json.loads`-parseable, and reflects the same results as table mode.

All specifications satisfied:
1. ✅ `--output-format` long-only option, default `table`.
2. ✅ Table mode byte-identical to before (status line + Summary + Detailed orgtbl).
3. ✅ JSON mode: stdout is exactly one JSON document; status line goes to stderr.
4. ✅ Top-level keys exactly `summary` + `detailed`; numeric types correct.
5. ✅ Invalid value → single stderr error line, exit code 2, no stdout JSON.
6. ✅ Only default report scope modified; subcommands untouched.
7. ✅ All 28 existing tests pass.
8. ✅ `-g` single/multi-column grouping works in both modes with correct JSON keys.

DONE
