$ cd /repo 2>/dev/null; .venv/bin/python -m ngxtop.ngxtop --no-follow -c repro/nginx.conf -v 2>&1 | grep -iv warning | grep -i "log_format\|access_log\|pattern" | head; echo "---with -l"; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/access.log -c repro/nginx.conf -v 2>&1 | grep -iv "warning\|re\." | head -20
INFO: access_log: stdin
INFO: log_format: combined
---with -l
INFO: access_log: repro/access.log
INFO: log_format: combined
INFO: query for "Summary:":
 SELECT
       count(1)                                    AS count,
       avg(bytes_sent)                             AS avg_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     ORDER BY count DESC
     LIMIT 10
INFO: query for "Detailed:":
 SELECT
       request_path,
       count(1)                                    AS count,
       avg(bytes_sent)                             AS avg_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',

[exit code: 0]