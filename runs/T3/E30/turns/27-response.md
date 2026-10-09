Now median shows 512.000 consistent with avg formatting. Now check the default combined format still works, and that the column also appears for combined.log (2 records).

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null | grep -A4 "Summary:"

Send.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null | grep -A3 "Summary:"</parameter>

Send (clean).

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null | grep -A3 "Summary:"
