READ ngxtop/utils.py

RUN cat tests/test_characterization.py | head -80

RUN .venv/bin/python -m pytest tests/ -q 2>&1 | tail -15

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>&1</｜｜DSML｜｜ parameter>
