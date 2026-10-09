$ .venv/bin/python -c "s=open('ngxtop/config_parser.py').read().splitlines(); [print(i, repr(l)) for i,l in enumerate(s[:8],1)]"
1 '"""'
2 'Nginx config parser and pattern builder.'
3 '"""'
4 'import os'
5 'import re'
6 'import subprocess'
7 ''
8 'from pyparsing import Literal, Word, ZeroOrMore, OneOrMore, Group, \\'

[exit code: 0]