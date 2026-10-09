I'll start by exploring the repository structure and understanding the existing code.

RUN ls -la && echo "---" && ls ngxtop/ tests/ repro/ 2>&1

RUN cat ngxtop/ngxtop.py

RUN cat ngxtop/config.py 2>/dev/null | head -100

RUN ls ngxtop/ && echo "===TESTS===" && ls tests/ && echo "===REPRO===" && ls repro/
