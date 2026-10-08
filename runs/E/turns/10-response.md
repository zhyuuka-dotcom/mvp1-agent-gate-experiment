Now let me run the repro.

RUN .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow 2>&1; echo "EXIT: $?"
