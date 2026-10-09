$ grep -n "add \|--a\|<var>\|<exp>\|extract_variables" ngxtop/ngxtop.py ngxtop/config_parser.py | head
ngxtop/ngxtop.py:5:    ngxtop [options] (print|top|avg|sum) <var> ...
ngxtop/ngxtop.py:10:    -l <file>, --access-log <file>  access log file to parse.
ngxtop/ngxtop.py:18:    -g <var>, --group-by <var>  group by variable [default: request_path]
ngxtop/ngxtop.py:19:    -w <var>, --having <expr>  having clause [default: 1]
ngxtop/ngxtop.py:20:    -o <var>, --order-by <var>  order of output for default query [default: count]
ngxtop/ngxtop.py:22:    -a <exp> ..., --a <exp> ...  add exp (must be aggregation exp: sum, avg, min, max, etc.) into output
ngxtop/ngxtop.py:83:from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern
ngxtop/ngxtop.py:506:    fields = arguments['<var>']
ngxtop/ngxtop.py:581:    access_log = arguments['--access-log']
ngxtop/ngxtop.py:598:        print('available variables:\n ', ', '.join(sorted(extract_variables(log_format))))

[exit code: 0]