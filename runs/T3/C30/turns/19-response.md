The malformed marker persists. The issue is likely my closing tag. Let me try using the exact literal tags shown in the instructions: `WRITE <path>` then `<<<FILE_CONTENTS` ... `FILE_CONTENTS`, without parameter decoration.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents">test</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ calls>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
