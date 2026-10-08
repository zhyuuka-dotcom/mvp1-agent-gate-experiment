$ cd /home/user 2>/dev/null; .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow; echo "EXIT=$?"
EXIT=127

[stderr]
bash: line 1: .venv/bin/python: No such file or directory

[exit code: 0]