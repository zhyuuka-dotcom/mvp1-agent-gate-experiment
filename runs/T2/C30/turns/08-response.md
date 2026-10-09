I now have enough understanding. The key insight:
- `report()` returns combined stdout text (status line + tables).
- In JSON mode, I need to emit status line to stderr, and JSON to stdout.
- The `build_processor` needs to know the group-by column and report queries to extract data.

Let me look at the config to understand how `arguments['--group-by']` is used with comma-separated grouping (bullet 8).

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cd /tmp/t2c30/repo && .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g remote_addr,status 2>/dev/null; echo "EXIT=$?"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
