#!/usr/bin/env python3
"""T2 E/C 臂请求执行器——exec_request_e + T2 丙校验器（D-014）。
与 runs/E/exec_request_e.py 唯一差异：VALIDATOR 指向 validate_plan_T2.py。
机制：与 C 完全一致（PLAN.md 门禁 + DSML 双格式 + 纯文本协议 + RUN/READ
不受限）；DONE 检测在前（exit 99），验收由循环驱动器 run_e.py 接管
（INDEPENDENT_ACCEPTANCE，四行回执作为该轮回填）。
用法（cwd=repo 根）: E_STATE=<state.json 路径> exec_request_e.py <response.md> <feedback.md>
退出码: 99=DONE；0=正常；98=空转
与 C 版的差异（仅两处，其余逐字）：STATE_PATH/VALIDATOR 改绝对路径
（E 运行仓不在 mvp1 目录树内，防 ../ 相对依赖）。
"""
import json, os, re, subprocess, sys

resp_path, fb_path = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
MVP1 = os.path.dirname(os.path.dirname(HERE))
STATE_PATH = os.environ.get("E_STATE", os.path.join(HERE, "state.json"))
VALIDATOR = os.path.join(MVP1, "runs", "T2", "validate_plan_T2.py")  # D-014 丙
text = open(resp_path, encoding="utf-8").read()
REPO = os.getcwd()

def load_state():
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH, encoding="utf-8"))
    return {"phase": "PRE_PLAN", "whitelist": [], "plan_attempts": 0,
            "plan_rejections": 0, "amendments": 0}

def save_state(st):
    json.dump(st, open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

parts, exec_log = [], []
st = load_state()

def emit(s):
    parts.append(s)

def safe_path(p):
    p = os.path.normpath(p)
    if p.startswith("/") or ".." in p.split(os.sep):
        return None
    return p

# ---------------- 计划门禁 WRITE 拦截（与 C 逐字同源） ----------------
def gated_write(p_raw, content):
    p = safe_path(p_raw)
    if p is None:
        emit(f"WRITE 错误: 路径越界: {p_raw}"); return "WRITE_PATHERR"
    if p == "PLAN.md":
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        if content is None:
            emit("错误: WRITE 块未闭合（缺少 FILE_CONTENTS 结束标记），内容未写入。")
            return "WRITE_TRUNCATED"
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        emit(f"WROTE PLAN.md ({len(content.encode('utf-8'))} bytes) —— 合同已提交，机械校验如下")
        r = subprocess.run(["python3", VALIDATOR, REPO, "PLAN.md"],
                           capture_output=True, text=True, timeout=60)
        try:
            verdict = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            emit("[PLAN_GATE: 内部错误——校验器输出无法解析]"); return "PLAN_ERR"
        st["plan_attempts"] += 1
        was = st["phase"]
        if verdict["pass"]:
            st["phase"] = "PLAN_APPROVED"
            st["whitelist"] = verdict["touch_set"]
            if was == "PLAN_APPROVED":
                st["amendments"] += 1
                tag = f"APPROVED (attempt #{st['plan_attempts']}, amendment #{st['amendments']})"
            else:
                tag = f"APPROVED (attempt #{st['plan_attempts']})"
            emit(f"[PLAN_GATE: {tag}]\nTOUCH_SET 冻结为 WRITE 白名单:\n" +
                 "\n".join(f"- {x}" for x in verdict["touch_set"]))
            save_state(st)
            return f"PLAN_APPROVED a{st['plan_attempts']}"
        else:
            st["plan_rejections"] += 1
            save_state(st)
            emit(f"[PLAN_GATE: REJECTED (attempt #{st['plan_attempts']})]\n未通过检查:\n" +
                 "\n".join(f"- {x}" for x in verdict["failures"]) +
                 "\n（该次提交已消耗一轮；可重新提交完整合同）")
            return f"PLAN_REJECTED a{st['plan_attempts']}"
    # 非 PLAN.md 写入
    if st["phase"] != "PLAN_APPROVED":
        emit("[WRITE 拒绝: PERMISSION_DENIED] 计划合同尚未通过——先按合同格式提交 PLAN.md"
             "（READ/RUN 不受此限）")
        return "WRITE_DENIED_NOPLAN"
    if p not in st["whitelist"]:
        emit(f"[WRITE 拒绝: PERMISSION_DENIED] 路径 {p} 不在 TOUCH_SET 白名单:\n" +
             "\n".join(f"- {x}" for x in st["whitelist"]) +
             "\n（扩清单须整体重交合同，记为 amendment）")
        return "WRITE_DENIED"
    if content is None:
        emit("错误: WRITE 块未闭合（缺少 FILE_CONTENTS 结束标记），内容未写入。")
        return "WRITE_TRUNCATED"
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    emit(f"WROTE {p} ({len(content.encode('utf-8'))} bytes)")
    return f"WRITE_OK {p}"

def do_read(p_raw):
    p = safe_path(p_raw)
    if p is None:
        emit(f"READ 错误: 路径越界: {p_raw}"); return "READ_PATHERR"
    if not os.path.isfile(p):
        emit(f"READ 错误: 文件不存在: {p}"); return "READ_MISS"
    c = open(p, encoding="utf-8", errors="replace").read()
    if len(c) > 30000:
        emit(c[:15000] + f"\n…[READ 截断：全文 {len(c)} 字符，前 15000]\n" + c[-10000:])
        return f"READ_TRUNC {p}"
    emit(c); return f"READ_OK {p} {len(c)}ch"

def do_run(cmd):
    # v5（C-T14 执行前落盘）：RUN 缺 command 参数 → 机械校验错误回执
    if not cmd or not cmd.strip():
        emit("RUN 错误: 缺少 command 参数（工具调用结构畸形）"); return "RUN_NOARG"
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

# --- DONE（检测在前，与 A/C 同序；验收由 run_e.py 接管） ---
if re.search(r"^DONE\s*$", text, re.M):
    print("DONE_DETECTED")
    sys.exit(99)

# --- DSML 原生工具调用（v3/v4 通道适配沿 A/C 同款） ---
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
        emit("[harness 注记: 存在无法解析的工具调用片段（畸形标记），已忽略]")
for name, body in invokes:
    params = dict((k, v) for k, v in DSML_PARAM.findall(body))
    if name == "RUN":
        exec_log.append(do_run(params.get("command", "")))
    elif name == "READ":
        p = params.get("path") or params.get("file") or params.get("target") or ""
        exec_log.append(do_read(p))
    elif name == "WRITE":
        p = params.get("path") or params.get("file") or ""
        c = params.get("content")
        if c is None:
            m2 = re.search(r"<<<FILE_CONTENTS\s*\n(.*?)\nFILE_CONTENTS", body, re.S)
            c = m2.group(1) + "\n" if m2 else None
        exec_log.append(gated_write(p, c))
    else:
        emit(f"未知工具: {name} 参数: {list(params.keys())}")
        exec_log.append(f"UNKNOWN_TOOL {name}")

# --- 纯文本协议（v1 兼容）---
if not invokes:
    m = re.search(r"^WRITE\s+(\S+)\s*\n<<<FILE_CONTENTS\s*\n(.*?)\nFILE_CONTENTS\s*$",
                  text, re.S | re.M)
    if m:
        exec_log.append(gated_write(m.group(1), m.group(2) + "\n"))
    else:
        m = re.search(r"^WRITE\s+(\S+)\s*\n<<<FILE_CONTENTS\s*\n(.*)$",
                  text, re.S | re.M)  # T2 修复：与闭合分支对齐补 re.M
                  # （T1 执行器此分支仅 re.S——文中截断写入落入 NO_ACTION；
                  #   差异见 selftest-quotes/selftest-results.txt case6 注记）
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
