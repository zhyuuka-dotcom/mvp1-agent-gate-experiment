$ .venv/bin/python -c "
from docopt import docopt
import ngxtop.ngxtop as n
" 2>/dev/null; grep -n "arguments\['--config'\]\|arguments\['info'\]\|build_source\|def process" ngxtop/ngxtop.py
444:    def process(self, records):
490:def process_log(lines, pattern, processor, arguments):
547:def build_source(access_log, arguments):
580:def process(arguments):
594:    if arguments['info']:
601:    source = build_source(access_log, arguments)

[exit code: 0]