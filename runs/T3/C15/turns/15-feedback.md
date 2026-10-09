$ FMT='$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'
.venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f "$FMT" 2>/dev/null; echo "EXIT=$?"
running for 0 seconds, 5 records processed: 6674.58 req/sec

Summary:
|   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+-------+-------+-------+-------|
|       5 |         1626.600 |     2 |     1 |     1 |     1 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+-------+-------+-------+-------|
| /              |       2 |         3584.000 |     2 |     0 |     0 |     0 |
| /old           |       1 |          300.000 |     0 |     1 |     0 |     0 |
| /img/a.png     |       1 |          512.000 |     0 |     0 |     0 |     1 |
| /api           |       1 |          153.000 |     0 |     0 |     1 |     0 |
EXIT=0

[exit code: 0]