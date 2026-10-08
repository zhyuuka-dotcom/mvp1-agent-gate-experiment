$ .venv/bin/python -c "
from ngxtop.config_parser import build_pattern
p = build_pattern('main')
print(repr(p.pattern))
line = open('repro/access.log').readline().strip()
print('MATCH:', p.match(line))
"
'main'
MATCH: None

[exit code: 0]