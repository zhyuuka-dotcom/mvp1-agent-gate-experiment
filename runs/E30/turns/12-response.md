I've reproduced the issue: 0 records processed. Now let me understand why. The format `main` is a name, not a format string. When passed via `-f main`, build_pattern treats "main" as a literal format string, not looking it up.

Let me check how `-f` is handled. In `process()`, `log_format` comes from `arguments['--log-format']`. When `access_log` is given, it never calls `detect_log_config`, so the format name `main` is never resolved to the actual format string.

Let me look at the other tests and utils.

READ ngxtop/utils.py

<tool_use_error>Wrong tool_name 1: 工具名必须是 'READ'，请求格式为：READ <path></tool_use_error>

READ ngxtop/utils.py
