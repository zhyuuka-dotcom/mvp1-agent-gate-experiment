My earlier outputs got jumbled. Let me read the characterization test and run the CLI cleanly.

READ tests/test_characterization.py

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow

RUN .venv/bin/python -m pytest tests/ -q 2>&1 | tail -6
