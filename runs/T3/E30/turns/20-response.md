All three edits landed. Now verify syntax and run the CLI against repro/access.log.

RUN .venv/bin/python -c "import ast; ast.parse(open('ngxtop/ngxtop.py').read()); print('syntax ok')"

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f main --no-follow

Send both (one per turn). First syntax.

RUN .venv/bin/python -c "import ast; ast.parse(open('ngxtop/ngxtop.py').read()); print('syntax ok')"
