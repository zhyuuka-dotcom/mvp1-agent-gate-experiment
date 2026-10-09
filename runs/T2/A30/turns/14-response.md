The last case shows `count: 0` because that custom format string lacks the leading fields combined.log has (the `combined` format's `$remote_addr - - [...` expects a remote_user field, so lines don't match that custom format). That's a data/format mismatch in my ad-hoc test, not a bug — the same would happen with table mode. Let me confirm parity with table mode for that exact command to be sure the JSON path and table path agree.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ parameter name="command" string="true">FMT='$remote_addr - - [$time_local] "$request" $status $bytes_sent'
echo "=== table ==="; .venv/bin/python -m ngxtop.ngxtop -f "$FMT" -l repro/combined.log --no-follow -g remote_addr 2>/dev/null
echo "=== json ==="; .venv/bin/python -m ngxtop.ngxtop -f "$FMT" -l repro/combined.log --no-follow -g remote_addr --output-format json 2>/dev/null
echo "=== git diff stat ==="; git diff --stat 2>/dev/null || true</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
