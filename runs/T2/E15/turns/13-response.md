I now understand the report structure. The `report()` method builds a status line and runs queries. I need to refactor so JSON mode produces structured data. Let me see the combined.log default output too.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g request_path 2>/dev/null
