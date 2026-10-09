Now I understand the structure. The `report()` method builds the output. I need to add JSON support. Let me look at the relevant lines and config_parser for the -g handling.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">grep -n "report\|DEFAULT_QUERIES\|--group-by\|output-format\|def process\|def build_processor" ngxtop/ngxtop.py | head -40</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
