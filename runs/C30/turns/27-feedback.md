$ ls -la PLAN.md 2>&1; echo "==="; cat PLAN.md 2>&1 | head -3
ls: cannot access 'PLAN.md': No such file or directory
===
cat: PLAN.md: No such file or directory

[exit code: 0]