#!/usr/bin/env python3
"""C 臂 PLAN 合同机械校验器（R1-R4，冻结协议实现）。
用法: validate_plan.py <repo_root> <plan.md>
输出: 单行 JSON {pass: bool, failures: [...], touch_set: [...]}
只做机械结构检查，不做任何任务质量评价。
"""
import json, os, re, sys

repo, plan_path = sys.argv[1], sys.argv[2]
text = open(plan_path, encoding="utf-8").read()
failures, touch_set = [], []

def sections(header):
    m = re.search(rf"^##\s*{header}\s*$(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    return m.group(1) if m else None

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

# ---- R1: TOUCH_SET ----
ts = sections("TOUCH_SET")
if ts is None:
    failures.append("R1: 缺 TOUCH_SET 节")
else:
    paths = re.findall(r"^-\s*(\S+)\s*$", ts, re.M)
    if not (1 <= len(paths) <= 5):
        failures.append(f"R1: TOUCH_SET 须 1~5 个文件，现有 {len(paths)}")
    for p in paths:
        if not os.path.isfile(os.path.join(repo, p)):
            failures.append(f"R1: 路径不存在: {p}")
    touch_set = paths

# ---- R2: ASSUMPTIONS ----
asum = sections("ASSUMPTIONS")
if asum is None:
    failures.append("R2: 缺 ASSUMPTIONS 节")
else:
    entries = re.split(r"(?=^- 假设[:：])", asum, flags=re.M)
    entries = [e for e in entries if e.strip()]
    if not entries:
        failures.append("R2: ASSUMPTIONS 无条目")
    files_seen = set()
    for idx, e in enumerate(entries, 1):
        if not re.search(r"^- 假设[:：]", e, re.M):
            failures.append(f"R2 条目{idx}: 缺「假设:」段")
        m = re.search(r"依据[:：]\s*(\S+?):(\d+)-(\d+)\s*\|\s*(.+)$", e, re.M)
        if not m:
            failures.append(f"R2 条目{idx}: 依据段格式须为「路径:起-止 | 逐字引文」")
            continue
        path, s, t, quote = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            failures.append(f"R2 条目{idx}: 依据文件不存在: {path}")
            continue
        files_seen.add(path)
        lines = open(full, encoding="utf-8", errors="replace").read().splitlines()
        seg = "\n".join(lines[s - 1:t]) if 1 <= s <= t <= len(lines) else None
        if seg is None:
            failures.append(f"R2 条目{idx}: 行区间 {s}-{t} 超出 {path}（共 {len(lines)} 行）")
        elif norm(quote) not in norm(seg):
            failures.append(f"R2 条目{idx}: 引文未在 {path}:{s}-{t} 逐字出现（空白归一化后比对）")
        if not re.search(r"验证[:：]", e):
            failures.append(f"R2 条目{idx}: 缺「验证:」段")
    if entries and len(files_seen) < 2:
        failures.append(f"R2: 依据文件跨条目仅覆盖 {len(files_seen)} 个（须 ≥2）")

# ---- R3: BEHAVIOR_DELTAS ----
bd = sections("BEHAVIOR_DELTAS")
if bd is None:
    failures.append("R3: 缺 BEHAVIOR_DELTAS 节")
else:
    entries = [e for e in re.split(r"(?=^- 增量[:：])", bd, flags=re.M) if e.strip()]
    if not entries:
        failures.append("R3: BEHAVIOR_DELTAS 无条目")
    for idx, e in enumerate(entries, 1):
        m = re.search(r"VERIFY[:：]\s*(.+)$", e, re.M)
        if not m or not m.group(1).strip():
            failures.append(f"R3 条目{idx}: VERIFY 缺失或为空")

# ---- R4: NON_GOALS ----
ng = sections("NON_GOALS")
if ng is None:
    failures.append("R4: 缺 NON_GOALS 节")
else:
    entries = [e for e in re.split(r"(?=^- 非目标[:：])", ng, flags=re.M) if e.strip()]
    if not entries:
        failures.append("R4: NON_GOALS 无条目")
    for idx, e in enumerate(entries, 1):
        m = re.search(r"GUARD[:：]\s*(.+)$", e, re.M)
        if not m or not m.group(1).strip():
            failures.append(f"R4 条目{idx}: GUARD 缺失或为空")
        else:
            g = m.group(1).strip()
            tokens = re.findall(r"[\w./-]+", g)
            if not (any(os.path.exists(os.path.join(repo, t)) for t in tokens) or len(tokens) >= 2):
                failures.append(f"R4 条目{idx}: GUARD 须指向真实存在的测试/命令")

# ---- R5: TEST_PLAN（存在即可）----
if sections("TEST_PLAN") is None or not sections("TEST_PLAN").strip():
    failures.append("R5: 缺 TEST_PLAN 节")

print(json.dumps({"pass": not failures, "failures": failures,
                  "touch_set": touch_set}, ensure_ascii=False))
sys.exit(0 if not failures else 1)
