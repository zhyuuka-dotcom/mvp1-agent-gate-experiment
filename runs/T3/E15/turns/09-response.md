No existing test asserts exact columns. Now I have enough. Let me write the plan.

Note the filter expression uses `eval(filter_exp, {}, r)`, so the median must be an SQL column in the report.

The cleanest approach: add a `med_bytes_sent` column via a scalar SQLite subquery. SQLite doesn't have MEDIAN built in. A common idiom: `(SELECT AVG(bytes_sent) FROM (SELECT bytes_sent FROM log ... ORDER BY bytes_sent LIMIT 2 - ...))`. But it's complex in a grouped query. Let me design the median SQL to work both for the whole table (Summary) and per-group (Detailed).

Standard SQLite median idiom per group:
```
(SELECT AVG(bytes_sent) FROM (SELECT bytes_sent FROM log AS l2 WHERE l2.<group>=log.<group> ORDER BY bytes_sent LIMIT 2 - (SELECT COUNT(*) FROM log AS l3 WHERE l3.<group>=log.<group>) % 2 OFFSET (SELECT (COUNT(*)-1)/2 FROM log AS l4 WHERE l4.<group>=log.<group>)))
```
This is doable but group-by embedding is fragile. A simpler robust approach used by many: define a SQLite aggregate `median` via `conn.create_aggregate`. Then both `median(bytes_sent)` in Summary and `median(bytes_sent)` in Detailed with GROUP BY work naturally. This is much cleaner.

Let me check the fixed group-by `%(--group-by)s`. I'll register a `median` aggregate function on the connection and use `median(bytes_sent) AS med_bytes_sent`.

Now, what should the column be named? The convention is `avg_bytes_sent` for `avg(bytes_sent)`. So `median(bytes_sent)` → convention suggests `med_bytes_sent` or `median_bytes_sent`. Given `avg_` abbreviation pattern, "median" abbreviated to "med" matches. But the task says "未指定的取值以仓库公开证据为准" (unspecified values governed by repo public evidence). There's no existing median evidence. I'll go with `med_bytes_sent` matching the `avg_` abbreviation style, but I should also consider `median_bytes_sent` is more readable. The `-a` CLI option lets users add `median(bytes_sent)` themselves. Let me check how `-a` parses to confirm the aggregate name convention.

Let me check config_parser and the `-a` handling.

RUN grep -n "add \|--a\|<var>\|<exp>\|extract_variables" ngxtop/ngxtop.py ngxtop/config_parser.py | head

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -n "add \|--a\|<var>\|<exp>\|extract_variables" ngxtop/ngxtop.py ngxtop/config_parser.py | head</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
