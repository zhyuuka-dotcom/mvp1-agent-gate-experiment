The PLAN.md looks correct. The quotes are stored as explicit substrings. The line 91 quote in the file: `       avg(bytes_sent)                             AS avg_bytes_sent,` — this appears correct (7 leading spaces).

Wait — maybe the harness strips the leading spaces of the quote when parsing? The rule says "去除首尾换行后 ≤120 字符" (only strips leading/trailing *newlines*), and "不做空白归一化". So my quote with leading spaces should be exact.

Hmm, but the quote in PLAN.md might have lost its leading spaces because the WRITE content had them. Looking at `cat` output, the quote line appears indented relative to "依据:". Let me check with cat -A whether those are real spaces and compare exactly.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">grep -n "avg(bytes_sent)" PLAN.md | cat -A</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ calls>
