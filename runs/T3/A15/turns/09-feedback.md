$ sed -n '60,210p' README.rst
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

    top remote_addr
    | remote_addr     |   count |
    |-----------------+---------|
    | 118.173.177.161 |      20 |
    | 110.78.145.3    |      16 |
    | 171.7.153.7     |      16 |
    | 180.183.67.155  |      16 |
    | 183.89.65.9     |      16 |
    | 202.28.182.5    |      16 |
    | 1.47.170.12     |      15 |
    | 119.46.184.2    |      15 |
    | 125.26.135.219  |      15 |
    | 125.26.213.203  |      15 |

List 4xx or 5xx responses together with HTTP referer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ ngxtop -i 'status >= 400' print request status http_referer
    running for 2 seconds, 28 records processed: 13.95 req/sec

    request, status, http_referer:
    | request   |   status | http_referer   |
    |-----------+----------+----------------|
    | -         |      400 | -              |

Parse apache log from remote server with `common` format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ ssh user@remote_server tail -f /var/log/apache2/access.log | ngxtop -f common
    running for 20 seconds, 1068 records processed: 53.01 req/sec

    Summary:
    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |---------+------------------+-------+-------+-------+-------|
    |    1068 |        28026.763 |  1029 |    20 |    19 |     0 |

    Detailed:
    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |------------------------------------------+---------+------------------+-------+-------+-------+-------|
    | /xxxxxxxxxx                              |     199 |        55150.402 |   199 |     0 |     0 |     0 |
    | /xxxxxxxx/xxxxx                          |     167 |        47591.826 |   167 |     0 |     0 |     0 |
    | /xxxxxxxxxxxxx/xxxxxx                    |      25 |         7432.200 |    25 |     0 |     0 |     0 |
    | /xxxx/xxxxx/x/xxxxxxxxxxxxx/xxxxxxx      |      22 |          698.727 |    22 |     0 |     0 |     0 |
    | /xxxx/xxxxx/x/xxxxxxxxxxxxx/xxxxxx       |      19 |         7431.632 |    19 |     0 |     0 |     0 |
    | /xxxxx/xxxxx/                            |      18 |         7840.889 |    18 |     0 |     0 |     0 |
    | /xxxxxxxx/xxxxxxxxxxxxxxxxx              |      15 |         7356.000 |    15 |     0 |     0 |     0 |
    | /xxxxxxxxxxx/xxxxxxxx                    |      15 |         9978.800 |    15 |     0 |     0 |     0 |
    | /xxxxx/                                  |      14 |            0.000 |     0 |    14 |     0 |     0 |
    | /xxxxxxxxxx/xxxxxxxx/xxxxx               |      13 |        20530.154 |    13 |     0 |     0 |     0 |

Parse Caddy server access log with JSON format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ ngxtop -l /var/log/caddy/access.log -f caddy
    running for 15 seconds, 234 records processed: 15.60 req/sec

    Summary:
    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |---------+------------------+-------+-------+-------+-------|
    |     234 |         5482.342 |   198 |    12 |    22 |     2 |

    Detailed:
    | request_path                        |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |-------------------------------------+---------+------------------+-------+-------+-------+-------|
    | /api/v1/users                       |      32 |          128.000 |    32 |     0 |     0 |     0 |
    | /images/logo.png                    |      28 |        24560.000 |    28 |     0 |     0 |     0 |
    | /blog/article-not-found             |      22 |         5621.000 |     0 |     0 |    22 |     0 |
    | /audiobooks                         |      21 |        16818.000 |    21 |     0 |     0 |     0 |
    | /v1/sessions/12345                  |      18 |           35.000 |    18 |     0 |     0 |     0 |
    | /static/css/main.css                |      17 |         1459.000 |    17 |     0 |     0 |     0 |
    | /static/js/app.js                   |      15 |         5824.000 |    15 |     0 |     0 |     0 |
    | /                                   |      12 |         3245.000 |     0 |    12 |     0 |     0 |
    | /api/v2/metrics                     |      10 |          873.000 |     8 |     0 |     0 |     2 |
    | /favicon.ico                        |       8 |         1246.000 |     8 |     0 |     0 |     0 |

Group by host (useful in multi-host setups)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ ngxtop -l /var/log/caddy/access.log -f caddy --group-by host
    running for 10 seconds, 156 records processed: 15.60 req/sec

    Summary:
    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |---------+------------------+-------+-------+-------+-------|
    |     156 |         7281.632 |   142 |     8 |     4 |     2 |

    Detailed:
    | host                |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
    |---------------------+---------+------------------+-------+-------+-------+-------|
    | api.example.com     |      75 |          124.533 |    73 |     0 |     0 |     2 |
    | static.example.net  |      42 |        16903.857 |    42 |     0 |     0 |     0 |
    | example.org         |      31 |         3791.258 |    19 |     8 |     4 |     0 |
    | imusic.br.com       |       8 |        16818.000 |     8 |     0 |     0 |     0 |


[exit code: 0]