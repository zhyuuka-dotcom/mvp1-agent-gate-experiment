Let me look at tests, especially characterization, and check for median-related conventions.

RUN grep -rn "median\|avg_bytes_sent\|bytes_sent" tests/ | head -40 && echo "===CHAR===" && sed -n '1,80p' tests/test_characterization.py

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -rn "median\|avg_bytes_sent\|bytes_sent" tests/ | head -40 && echo "===CHAR===" && sed -n '1,80p' tests/test_characterization.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
