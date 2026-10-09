Now I understand the output format. The request asks to add median of bytes_sent in the report. The natural convention: add a `med_bytes_sent` column next to `avg_bytes_sent` in both Summary and Detailed tables. SQLite has no built-in median, but there are workarounds. Let me check README for column naming conventions.

RUN grep -n "avg_bytes_sent\|bytes_sent\|median\|Summary\|Detailed\|column" README.rst | head -30

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -n "avg_bytes_sent\|bytes_sent\|median\|Summary\|Detailed\|column" README.rst | head -30</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
