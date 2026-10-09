$ cd /repo 2>/dev/null; echo "=== combined ==="; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/combined.log -f combined 2>&1 | grep -v Warning | grep -v "re\." | tail -12; echo; echo "=== access.log custom format (5 records) median should be 512 ==="; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/access.log -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' 2>&1 | grep -v Warning | grep -v "re\." | tail -12
=== combined ===
running for 0 seconds, 2 records processed: 15709.00 req/sec

Summary:
|   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+---------------------+-------+-------+-------+-------|
|       2 |         2636.500 |            2636.500 |     1 |     0 |     1 |     0 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+---------------------+-------+-------+-------+-------|
| /api           |       1 |          153.000 |                 153 |     0 |     0 |     1 |     0 |
| /              |       1 |         5120.000 |                5120 |     1 |     0 |     0 |     0 |

=== access.log custom format (5 records) median should be 512 ===
Summary:
|   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|---------+------------------+---------------------+-------+-------+-------+-------|
|       5 |         1626.600 |                 512 |     2 |     1 |     1 |     1 |

Detailed:
| request_path   |   count |   avg_bytes_sent |   median_bytes_sent |   2xx |   3xx |   4xx |   5xx |
|----------------+---------+------------------+---------------------+-------+-------+-------+-------|
| /              |       2 |         3584.000 |            3584.000 |     2 |     0 |     0 |     0 |
| /old           |       1 |          300.000 |             300.000 |     0 |     1 |     0 |     0 |
| /img/a.png     |       1 |          512.000 |             512.000 |     0 |     0 |     0 |     1 |
| /api           |       1 |          153.000 |             153.000 |     0 |     0 |     1 |     0 |

[exit code: 0]