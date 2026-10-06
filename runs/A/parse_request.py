#!/usr/bin/env python3
"""A 臂请求解析器——从 agent 回复中机械提取工具请求（不做任何语义加工）。
用法: parse_request.py <response.md>
输出: 单行 JSON {action, arg, write_size} 或 {action: NONE|WRITE_TRUNCATED}
"""
import json, re, sys

text = open(sys.argv[1], encoding="utf-8").read()

# DONE：独立行
if re.search(r"^DONE\s*$", text, re.M):
    print(json.dumps({"action": "DONE"}))
    sys.exit(0)

# WRITE 块
m = re.search(r"^WRITE\s+(\S+)\s*\n<<<FILE_CONTENTS\s*\n(.*?)\nFILE_CONTENTS\s*$",
              text, re.S | re.M)
if m:
    content = m.group(2) + "\n"
    print(json.dumps({"action": "WRITE", "arg": m.group(1), "write_size": len(content)}))
    sys.exit(0)
m = re.search(r"^WRITE\s+(\S+)\s*\n<<<FILE_CONTENTS\s*\n(.*)$", text, re.S)
if m:
    print(json.dumps({"action": "WRITE_TRUNCATED", "arg": m.group(1)}))
    sys.exit(0)

# READ / RUN（取最后一个匹配——回复末尾的请求是最终意图）
reads = re.findall(r"^READ\s+(\S+)\s*$", text, re.M)
runs = re.findall(r"^RUN\s+(.+)$", text, re.M)
if reads:
    print(json.dumps({"action": "READ", "arg": reads[-1]}))
    sys.exit(0)
if runs:
    print(json.dumps({"action": "RUN", "arg": runs[-1].strip()}))
    sys.exit(0)

print(json.dumps({"action": "NONE"}))
