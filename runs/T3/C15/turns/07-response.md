Let me check the other tests and the remaining test files to understand conventions around the CLI output.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">grep -rn "bytes_sent\|median\|percentile\|Summary\|Detailed\|DEFAULT_QUERIES\|DEFAULT_FIELDS" tests/ | grep -v test_characterization | head -40</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
<｜｜DSML｜｜ calls>
</｜｜DSML｜｜ invoke name="READ">
<｜｜DSML｜｜ parameter name="path" string="true">README.rst</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ calls>
</｜｜DSML｜｜ calls>
