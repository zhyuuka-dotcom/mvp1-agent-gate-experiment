Now let me look at the characterization test and confirm behavior.

RUN cat tests/test_characterization.py

RUN .venv/bin/python -m pytest tests/ -q 2>&1 | tail -8

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>&1</｜｜DSML｜｜ parameter>
