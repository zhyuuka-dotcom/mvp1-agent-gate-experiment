Let me check tests that assert exact column structure so I don't break them, and check the avg/sum subcommands handling of aliases.

RUN grep -rn "avg_bytes_sent\|\"Detail\|'Detail\|Summary\|med_" tests/ && echo "===" && grep -rn "DEFAULT_QUERIES\|med_" ngxtop/

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -rn "avg_bytes_sent\|\"Detail\|'Detail\|Summary\|med_" tests/ && echo "===" && grep -rn "DEFAULT_QUERIES\|med_" ngxtop/</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
