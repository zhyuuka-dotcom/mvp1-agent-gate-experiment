I keep accidentally including stray text. Let me run commands cleanly, one per request.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow

RUN .venv/bin/python -m pytest tests/ -q
