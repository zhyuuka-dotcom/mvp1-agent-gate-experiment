Now I have a clear picture. Let me check the existing characterization tests to understand expected behavior and check the `--no-follow` flow, plus the docopt options section.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">
cat tests/test_characterization.py | head -60; echo "==="; grep -rn "output-format\|output_format\|report()\|sqlite3.Row\|row_factory" tests/ ngxtop/</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
