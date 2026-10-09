Now let me look at the test files to understand existing conventions around byte stats, and check README's documented report.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">grep -rn "bytes_sent\|avg_bytes_sent\|median" README.rst tests/ ngxtop/ | grep -v ".venv"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
