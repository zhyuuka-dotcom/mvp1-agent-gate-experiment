The multiline conf read earlier got mixed up. Let me check it and run the repro separately.

READ repro/nginx_multiline.conf

RUN .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow 2>&1; echo "EXIT: $?"
