$ sed -n '60,100p' README.rst; echo "=== try -f with full format string ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' 2>/dev/null
        -p <filter-expression>, --pre-filter <filter-expression> in-filter expression to check in pre-parsing phase.
        
        Supported log formats: combined (default), common, caddy (for Caddy JSON access logs)

Samples
-------

Default output
~~~~~~~~~~~~~~

::

    $ ngxtop
    running for 411 seconds, 64332 records processed: 156.60 req/sec

    Summary:
    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |---------+------------------+-------+-------+-------+-------|
    |   64332 |         2775.251 | 61262 |  2994 |    71 |     5 |

    Detailed:
    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |------------------------------------------+---------+------------------+-------+-------+-------+-------|
    | /abc/xyz/xxxx                            |   20946 |          434.693 | 20935 |     0 |    11 |     0 |
    | /xxxxx.json                              |    5633 |         1483.723 |  5633 |     0 |     0 |     0 |
    | /xxxxx/xxx/xxxxxxxxxxxxx                 |    3629 |         6835.499 |  3626 |     0 |     3 |     0 |
    | /xxxxx/xxx/xxxxxxxx                      |    3627 |        15971.885 |  3623 |     0 |     4 |     0 |
    | /xxxxx/xxx/xxxxxxx                       |    3624 |         7830.236 |  3621 |     0 |     3 |     0 |
    | /static/js/minified/utils.min.js         |    3031 |         1781.155 |  2104 |   927 |     0 |     0 |
    | /static/js/minified/xxxxxxx.min.v1.js    |    2889 |         2210.235 |  2068 |   821 |     0 |     0 |
    | /static/tracking/js/xxxxxxxx.js          |    2594 |         1325.681 |  1927 |   667 |     0 |     0 |
    | /xxxxx/xxx.html                          |    2521 |          573.597 |  2520 |     0 |     1 |     0 |
    | /xxxxx/xxxx.json                         |    1840 |          800.542 |  1839 |     0 |     1 |     0 |

View top source IPs of clients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ ngxtop top remote_addr
    running for 20 seconds, 3215 records processed: 159.62 req/sec
=== try -f with full format string ===
running for 0 seconds, 5 records processed: 6215.63 req/sec

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

[exit code: 0]