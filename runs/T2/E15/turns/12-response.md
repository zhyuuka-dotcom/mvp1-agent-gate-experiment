I must stop including the trailing junk. Let me send clean commands only.

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow

RUN .venv/bin/python -m ngxtop.ngxtop -f combined -l repro/access.log --no-follow

RUN .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g remote_addr,status
