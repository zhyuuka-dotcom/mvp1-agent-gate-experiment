Now let me look at the tests and utils, and check what tests reference report.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cat ngxtop/utils.py && echo "=== TESTS ===" && grep -rn "report\|output.format\|print(processor" tests/ | head -40</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
