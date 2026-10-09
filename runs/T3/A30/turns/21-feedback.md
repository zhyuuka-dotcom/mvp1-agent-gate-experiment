$ cd /repo 2>/dev/null; echo "=== -a add median exp ==="; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/combined.log -f combined -a 'median(bytes_sent)' 2>&1 | grep -v Warning | grep -v "re\." | tail -8; echo "=== group-by host custom ==="; FMT='$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/access.log -f "$FMT" -g host 2>&1 | grep -v Warning | grep -v "re\." | tail -8
=== -a add median exp ===
|---------+------------------+---------------------+-------+-------+-------+-------|
|       2 |         2636.500 |            2636.500 |     1 |     0 |     1 |     0 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+---------------------+-------+-------+-------+-------|
| /api           |       1 |          153.000 |                 153 |     0 |     0 |     1 |     0 |
| /              |       1 |         5120.000 |                5120 |     1 |     0 |     0 |     0 |
=== group-by host custom ===
|---------+------------------+---------------------+-------+-------+-------+-------|
|       5 |         1626.600 |                 512 |     2 |     1 |     1 |     1 |

Detailed:
| host            |   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|-----------------+---------+------------------+---------------------+-------+-------+-------+-------|
| example.com     |       4 |         1905.250 |            1174.000 |     2 |     1 |     1 |     0 |
| api.example.com |       1 |          512.000 |             512.000 |     0 |     0 |     0 |     1 |

[exit code: 0]