#!/usr/bin/env python3
"""A 臂请求执行器 v2——支持纯文本协议 + DeepSeek 原生 DSML 工具调用标记。
机械执行，输出原样回执到 feedback 文件。多 invoke 顺序执行、回执拼接（真实 agent 平台语义）。
用法（cwd=repo 根）: exec_request.py <response.md> <feedback.md>
退出码: 99=DONE；0=正常；98=无请求空转
v2 变更（执行 turn 1 请求前落盘，非事后改）：模型首答即用 DSML 原生标记，
纯文本协议解析器无法读取——扩展为双格式解析，属 harness 通道适配，零语义干预。
"""
import json, os, re, subprocess, sys

resp_path, fb_path = sys.argv[1], sys.argv[2]
text = open(resp_path, encoding="utf-8").read()
REPO = os.getcwd()

parts = []

def emit(s):
    parts.append(s)

def safe_path(p):
    p = os.path.normpath(p)
    if p.startswith("/") or ".." in p.split(os.sep):
        return None
    return p

def do_read(p_raw):
    p = safe_path(p_raw)
    if p is None:
        emit(f"READ 错误: 路径越界: {p_raw}"); return "READ_PATHERR"
    if not os.path.isfile(p):
        emit(f"READ 错误: 文件不存在: {p}"); return "READ_MISS"
    c = open(p, encoding="utf-8", errors="replace").read()
    if len(c) > 30000:
        emit(c[:15000] + f"\n…[READ 截断：全文 {len(c)} 字符，前 15000]\n" + c[-3000:])
        return f"READ_TRUNC {p}"
    emit(c); return f"READ_OK {p} {len(c)}ch"

def do_run(cmd):
    if re.search(r"rm\s+-rf\s+/(?!tmp|home)|mkfs|shutdown|reboot", cmd):
        emit(f"RUN 拒绝: 命令被安全策略拦截: {cmd}"); return "RUN_BLOCKED"
    try:
        r = subprocess.run(["bash", "-c", cmd], cwd=REPO, capture_output=True,
                           text=True, timeout=120)
        out = (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
        rc = r.returncode
    except subprocess.TimeoutExpired:
        out, rc = "[超时：命令超过 120 秒被终止]", -999
    if len(out) > 8000:
        out = out[:6000] + f"\n…[RUN 输出截断：全长 {len(out)} 字符]\n" + out[-1000:]
    emit(f"$ {cmd}\n{out}\n[exit code: {rc}]")
    return f"RUN_OK rc={rc} out={len(out)}ch"

def do_write(p_raw, content):
    p = safe_path(p_raw)
    if p is None:
        emit(f"WRITE 错误: 路径越界: {p_raw}"); return "WRITE_PATHERR"
    if content is None:
        emit("错误: WRITE 缺少内容参数。"); return "WRITE_NOCONTENT"
    if not content.endswith("\n"):
        content += "\n"
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    emit(f"WROTE {p} ({len(content.encode('utf-8'))} bytes)")
    return f"WRITE_OK {p} {len(content.encode('utf-8'))}B"

# --- DONE ---
if re.search(r"^DONE\s*$", text, re.M):
    print("DONE_DETECTED")
    sys.exit(99)

exec_log = []

# --- DSML 原生工具调用 ---
# v3（T10 执行前落盘）：模型闭合标签出现缺斜杠形态 `<｜｜DSML｜｜ invoke>`，
# 通道适配为两种闭合均可；孤儿参数片段（无 invoke 头）→ 机械注记不猜测语义。
DSML_INVOKE = re.compile(
    r"<｜｜DSML｜｜ invoke name=\"(\w+)\">(.*?)</?｜｜DSML｜｜ invoke>", re.S)
DSML_PARAM = re.compile(
    r"<｜｜DSML｜｜ parameter name=\"(\w+)\"[^>]*>(.*?)</｜｜DSML｜｜ parameter>", re.S)
DSML_ORPHAN_PARAM = re.compile(
    r"<｜｜DSML｜｜ parameter name=\"(\w+)\"[^>]*>(.*?)</｜｜DSML｜｜ parameter>")
invokes = DSML_INVOKE.findall(text)
invoked_spans = [m.span() for m in DSML_INVOKE.finditer(text)]
for m in DSML_ORPHAN_PARAM.finditer(text):
    if not any(s <= m.start() < e for s, e in invoked_spans):
        emit(f"[harness 注记: 存在无法解析的工具调用片段（畸形标记），已忽略]")
for name, body in invokes:
    params = dict((k, v) for k, v in DSML_PARAM.findall(body))
    if name == "RUN":
        cmd = params.get("command", "")
        exec_log.append(do_run(cmd))
    elif name == "READ":
        p = params.get("path") or params.get("file") or params.get("target") or ""
        exec_log.append(do_read(p))
    elif name == "WRITE":
        p = params.get("path") or params.get("file") or ""
        c = params.get("content")
        if c is None:
            # v4（T12 执行前落盘）：模型将 <<<FILE_CONTENTS 标记置于 DSML 外壳内、
            # 其后仍有协议尾行——内容提取改在 invoke 体内非锚定搜索
            m2 = re.search(r"<<<FILE_CONTENTS\s*\n(.*?)\nFILE_CONTENTS", body, re.S)
            c = m2.group(1) + "\n" if m2 else None
        exec_log.append(do_write(p, c))
    else:
        emit(f"未知工具: {name} 参数: {list(params.keys())}")
        exec_log.append(f"UNKNOWN_TOOL {name}")

# --- 纯文本协议（v1 兼容）---
if not invokes:
    m = re.search(r"^WRITE\s+(\S+)\s*\n<<<FILE_CONTENTS\s*\n(.*?)\nFILE_CONTENTS\s*$",
                  text, re.S | re.M)
    if m:
        exec_log.append(do_write(m.group(1), m.group(2) + "\n"))
    else:
        m = re.search(r"^WRITE\s+(\S+)\s*\n<<<FILE_CONTENTS\s*\n(.*)$", text, re.S)
        if m:
            emit("错误: WRITE 块未闭合（缺少 FILE_CONTENTS 结束标记），内容未写入。")
            exec_log.append("WRITE_TRUNCATED")
        else:
            reads = re.findall(r"^READ\s+(\S+)\s*$", text, re.M)
            runs = re.findall(r"^RUN\s+(.+)$", text, re.M)
            if reads:
                exec_log.append(do_read(reads[-1]))
            elif runs:
                exec_log.append(do_run(runs[-1].strip()))

with open(fb_path, "w", encoding="utf-8") as f:
    f.write("\n".join(parts) if parts else
            "（未识别到工具请求。请发出 READ / RUN / WRITE 请求，或单独一行 DONE。）")

print("; ".join(exec_log) if exec_log else "NO_ACTION")
sys.exit(98 if not exec_log else 0)
