Now I get a parseable response — the WRITE was received but the format was wrong. The harness expects the literal format:

```
WRITE <path>
<<<FILE_CONTENTS
...content...
FILE_CONTENTS
```

I need to emit it as raw text, not as a parameterized invoke. Let me write it directly.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents">placeholder</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ calls>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
