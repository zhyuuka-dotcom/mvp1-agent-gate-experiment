These tests just check substrings — safe. Now implement. I'll add `median_bytes_sent` as a column next to `avg_bytes_sent` in both Summary and Detailed. SQLite lacks a median function, so I need a subquery/correlated expression.

A common approach for median in SQLite: use a subquery computing the middle value(s). Since we can't easily do it inline per group, I can use a correlated expression. Let me think: for each row, median over the whole table (Summary) or over the group (Detailed).

Approach: define a SQL snippet. For the whole table:
```sql
(SELECT avg(bytes_sent) FROM (SELECT bytes_sent FROM log ORDER BY bytes_sent LIMIT 2 - (SELECT count(1) FROM log) % 2 OFFSET (SELECT (count(1)-1)/2 FROM log)))
```
That computes median simply.

For grouped (Detailed), we need median per group. Use correlated subquery referencing the group's value. A robust generic method:

```sql
(SELECT avg(bytes_sent) FROM (
   SELECT bytes_sent FROM log AS l2
   WHERE l2.<group> = log.<group>
   ORDER BY bytes_sent
   LIMIT 2 - (SELECT count(1) FROM log l3 WHERE l3.<group>=log.<group>) % 2
   OFFSET (SELECT (count(1)-1)/2 FROM log l4 WHERE l4.<group>=log.<group>)
))
```

But group-by can be an expression/variable. Simpler: since the report queries already GROUP BY, I can compute median via a window-free correlated subquery that doesn't need the group key explicitly — but SQL doesn't let correlated subquery inherit group easily without key.

Alternative cleaner approach: register a custom SQLite aggregate function `median` in SQLProcessor via `conn.create_aggregate`. That's the cleanest and works for both grouped and ungrouped, and can accept DISTINCT. Let me implement a median aggregate in Python and register it.

SQLite `create_aggregate("median", 1, MedianAggregate)`. Then use `median(bytes_sent) AS median_bytes_sent`.

But there's a subtlety: the table is populated before report; registering on the connection is fine. Let's implement.

Let me write the median aggregate class and add to DEFAULT_QUERIES.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="READ">
<｜｜DSML｜｜ parameter name="path">ngxtop/utils.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
