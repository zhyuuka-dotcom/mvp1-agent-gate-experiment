My multi-field calls keep getting mangled. It seems only single-parameter calls survive. Let me issue a clean single-command RUN.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -n 'avg(bytes_sent)' PLAN.md | cat -A</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ calls>
