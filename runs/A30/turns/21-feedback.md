$ git stash 2>&1 | tail -1; .venv/bin/python -m ngxtop.ngxtop -f common -l repro/combined.log --no-follow 2>&1 | grep "records processed"; git stash pop 2>&1 | tail -1
fatal: not a git repository (or any of the parent directories): .git
running for 0 seconds, 0 records processed: 0.00 req/sec
fatal: not a git repository (or any of the parent directories): .git

[exit code: 0]