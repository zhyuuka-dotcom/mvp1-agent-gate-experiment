<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">FMT='$remote_addr - - [$time_local] "$request" $status $bytes_sent'
echo "=== table ==="; .venv/bin/python -m ngxtop.ngxtop -f "$FMT" -l repro/combined.log --no-follow -g remote_addr 2>/dev/null
echo "=== json ==="; .venv/bin/python -m ngxtop.ngxtop -f "$FMT" -l repro/combined.log --no-follow -g remote_addr --output-format json 2>/dev/null</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
