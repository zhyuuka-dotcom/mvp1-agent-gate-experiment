Now let me reproduce the issue with the multiline format.

RUN cd /Users/z/Desktop/repos/ngxtop 2>/dev/null; .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow 2>&1 | head -30

<tool_use_error>Wrong tool_name 2: 命令必须以 .venv/bin/python、pytest 等允许的前缀开头且不含 &&、;、| 等连接符。请拆分为单个命令。</tool_use_error>

RUN .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow
