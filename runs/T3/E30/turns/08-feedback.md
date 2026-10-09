$ sed -n '75,110p' ngxtop/ngxtop.py | cat -A
try:$
    import urlparse$
except ImportError:$
    import urllib.parse as urlparse$
$
from docopt import docopt$
import tabulate$
$
from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern$
from .utils import error_exit$
$
$
DEFAULT_QUERIES = [$
    ('Summary:',$
     '''SELECT$
       count(1)                                    AS count,$
       avg(bytes_sent)                             AS avg_bytes_sent,$
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',$
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',$
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',$
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'$
     FROM log$
     ORDER BY %(--order-by)s DESC$
     LIMIT %(--limit)s'''),$
$
    ('Detailed:',$
     '''SELECT$
       %(--group-by)s,$
       count(1)                                    AS count,$
       avg(bytes_sent)                             AS avg_bytes_sent,$
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',$
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',$
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',$
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'$
     FROM log$
     GROUP BY %(--group-by)s$

[exit code: 0]