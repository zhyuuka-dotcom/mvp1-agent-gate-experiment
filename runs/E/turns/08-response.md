Now let me reproduce the issue. The user runs with `-f main -l access.log --no-follow`.

RUN .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow 2>&1; echo "EXIT: $?"

Let me also test with the multiline conf and see what happens.

RUN cat repro/nginx_multiline.conf; echo "==="; .venv/bin/python -c "
from ngxtop.config_parser import build_pattern, extract_variables
p = build_pattern('main')
print(repr(p.pattern))
print(list(extract_variables('main')))
"
