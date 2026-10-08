`common` gives 0 records for combined.log, which is expected since combined.log lacks the `$http_x_forwarded_for` field. Let's verify that's pre-existing behavior (not a regression).

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">git stash 2>&1 | tail -1; .venv/bin/python -m ngxtop.ngxtop -f common -l repro/combined.log --no-follow 2>&1 | grep "records processed"; git stash pop 2>&1 | tail -1</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
