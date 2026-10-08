The gate requires existing paths and exact quoted lines. Let me get the exact lines and use an existing test file instead.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">echo "=== ngxtop.py 11-12 ==="; sed -n '11,12p' ngxtop/ngxtop.py; echo "=== config_parser.py 78-90 ==="; sed -n '78,90p' ngxtop/config_parser.py; echo "=== ngxtop.py 580-588 ==="; sed -n '580,588p' ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
