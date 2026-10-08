Now I understand the architecture. The key issue: when user passes `-f main` where `main` is a named log_format, but also `-l` access log, there is no config parsing to resolve the name `main` into its format string. 

Let me verify my understanding by testing with the actual format string: `detect_log_config` calling `get_log_formats`. Let me also test the config path.

Let me test the config detection path:

RUN .venv/bin/python -m ngxtop.ngxtop --config repro/nginx_multiline.conf --no-follow -l repro/access.log

<tool_use_error>Wrong tool_name 2: 命令必须以 .venv/bin/python、pytest 等允许的前缀开头且不含 &&、;| 等连接符。拆分为单个命令。</tool_use_error>

RUN .venv/bin/python -m ngxtop.ngxtop --config repro/nginx_multiline.conf --no-follow

<tool_use_error>Wrong tool_name 2: 命令必须以 .venv/bin/python、pytest 等允许的前缀开头且不含 &&、;| 等连接符。拆分为单个命令。</tool_use_error>

RUN .venv/bin/python -m ngxtop.ngxtop --config repro/nginx_multiline.conf --no-follow

<tool_use_error>Wrong tool_name 2: 命令必须以 .venv/bin/python、pytest 等允许的前缀开头且不含 &&、;| 等连接符。拆分为单个命令。</tool_use_error>

*（以上重复内容为工具误用，忽略）*

RUN .venv/bin/python -m ngxtop.ngxtop --config repro/nginx_multiline.conf
