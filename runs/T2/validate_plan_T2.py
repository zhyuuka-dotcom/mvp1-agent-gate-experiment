#!/usr/bin/env python3
"""T2 PLAN 合同机械校验器（R1-R4，D-014 丙条款实现）。
与 T1 版（runs/C/validate_plan.py）的差异（均为 D-014 授权/隐含）：
  R1-T2：TOUCH_SET 路径存在 或 父目录存在（新建文件可入白名单——
          D-014(a)(d) 新建豁免+豁免用例"过"的启用条件；父目录检查
          保留防拼错保护。T1 原案=路径必须存在）
  R2-T2（丙）：TOUCH_SET 每个既有（将修改）文件须 ≥1 条有效单行引文
          ——单行（内部无换行）、首尾换行 trim 后 ≤120 字符、为该文件
          内容 exact substring（逐字，不做空白归一化）；新建文件豁免；
          多引不拒；不满足=合同整体拒。
          行区间字段保留为依据记录格式，不参与机械校验（D-014(b) 规格）。
  R3/R4/R5 与 T1 逐字相同。
用法: validate_plan_T2.py <repo_root> <plan.md>
输出: 单行 JSON {pass: bool, failures: [...], touch_set: [...]}
"""
import json, os, re, sys

repo, plan_path = sys.argv[1], sys.argv[2]
text = open(plan_path, encoding="utf-8").read()
failures, touch_set = [], []

def sections(header):
    m = re.search(rf"^##\s*{header}\s*$(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    return m.group(1) if m else None

# ---- R1: TOUCH_SET（T2：存在 或 父目录存在）----
ts = sections("TOUCH_SET")
if ts is None:
    failures.append("R1: 缺 TOUCH_SET 节")
else:
    paths = re.findall(r"^-\s*(\S+)\s*$", ts, re.M)
    if not (1 <= len(paths) <= 5):
        failures.append(f"R1: TOUCH_SET 须 1~5 个文件，现有 {len(paths)}")
    for p in paths:
        full = os.path.join(repo, p)
        if os.path.isfile(full):
            continue
        parent = os.path.dirname(full)
        if os.path.isdir(parent):
            continue  # 新建文件（D-014(a) 豁免路径）
        failures.append(f"R1: 路径不存在且父目录不存在: {p}")
    touch_set = paths

# ---- R2: ASSUMPTIONS（T2 丙：单行短引文）----
def quote_of(entry):
    """取条目引文区：依据行 | 之后至下一个 验证: 行（或条目末）。"""
    m = re.search(r"依据[:：]\s*(\S+?):(\d+)-(\d+)\s*\|", entry, re.M)
    if not m:
        return None, None
    path = m.group(1)
    rest = entry[m.end():]
    vm = re.search(r"^[ \t]*验证[:：]", rest, re.M)  # 模板验证行带缩进
    block = rest[:vm.start()] if vm else rest
    quote = block.strip()
    return path, quote

def quote_valid(quote, content):
    """D-014(b)：单行（内部无换行）+ trim 后 ≤120 + exact substring。"""
    if quote is None or quote == "":
        return False
    if "\n" in quote or "\r" in quote:
        return False  # 多行文本——不是单行
    if len(quote) > 120:
        return False
    return quote in content

asum = sections("ASSUMPTIONS")
valid_quotes = {}  # path -> [quotes...]（有效引文按文件归集）
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
        path, quote = quote_of(e)
        if path is None:
            failures.append(f"R2 条目{idx}: 依据段格式须为「路径:起-止 | 单行引文」")
            continue
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            failures.append(f"R2 条目{idx}: 依据文件不存在: {path}")
            continue
        files_seen.add(path)
        content = open(full, encoding="utf-8", errors="replace").read()
        if quote_valid(quote, content):
            valid_quotes.setdefault(path, []).append(quote)
        # 无效引文不单独拒（D-014(b) 多引不拒——宽松侧）；仅影响覆盖判定
        if not re.search(r"验证[:：]", e):
            failures.append(f"R2 条目{idx}: 缺「验证:」段")
    if entries and len(files_seen) < 2:
        failures.append(f"R2: 依据文件跨条目仅覆盖 {len(files_seen)} 个（须 ≥2）")

# 丙覆盖判定：TOUCH_SET 每个既有（将修改）文件 ≥1 条有效引文
for p in touch_set:
    full = os.path.join(repo, p)
    if os.path.isfile(full) and not valid_quotes.get(p):
        failures.append(
            f"R2(丙): TOUCH_SET 既有文件 {p} 缺有效引文"
            f"（单行、trim 后 ≤120 字符、文件内容精确子串；新建文件豁免）")

# ---- R3: BEHAVIOR_DELTAS（与 T1 逐字同）----
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

# ---- R4: NON_GOALS（与 T1 逐字同）----
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

# ---- R5: TEST_PLAN（存在即可，与 T1 同）----
if sections("TEST_PLAN") is None or not sections("TEST_PLAN").strip():
    failures.append("R5: 缺 TEST_PLAN 节")

print(json.dumps({"pass": not failures, "failures": failures,
                  "touch_set": touch_set}, ensure_ascii=False))
sys.exit(0 if not failures else 1)
