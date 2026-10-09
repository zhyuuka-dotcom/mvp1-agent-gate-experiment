#!/usr/bin/env python3
"""T2 循环驱动器（序列 v8：PI 批准后启动；参数全同 T1，零干预）。

用法: python3 run_t2.py <A|C|E> [run_root=/tmp/t2-<arm>] [cap=15]
- A：executor=runs/A/exec_request.py（无门禁）；DONE→离线验收→结束
- C：executor=runs/T2/exec_request_T2.py（丙门禁）；DONE→离线验收→结束
- E：同 C + INDEPENDENT_ACCEPTANCE 回执回填循环（PASS→结束）
mechanics：runs/T2/mechanics_T2_{A,C,E}[_final].md（A=T1 冻结原文；
C/E=丙终文）；TASK=tasks/T2/task.md；验收配置=runs/E/acceptance_config_T2.json。
第二轮@30：cap=30 + cap 行窄正则改写（D-015 §4 修复；T1 先例=预改写
文件方案，本驱动=运行时改写，快照均=实际发送文本）。
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
MVP1 = HERE.parent.parent
LEARNHUB = MVP1.parent.parent
DS_AGENT = LEARNHUB / "bin" / "ds-agent.sh"
FROZEN = MVP1 / "repo_frozen"
TASK = MVP1 / "tasks" / "T2" / "task.md"
ACCEPT_CFG = MVP1 / "runs" / "E" / "acceptance_config_T2.json"

sys.path.insert(0, str(MVP1 / "runs" / "E"))
from independent_acceptance import run_acceptance  # noqa: E402

ARM = sys.argv[1] if len(sys.argv) > 1 else "E"
RUN = Path(sys.argv[2] if len(sys.argv) > 2 else f"/tmp/t2{ARM.lower()}").resolve()
CAP = int(sys.argv[3]) if len(sys.argv) > 3 else 15
MECH = {
    "A": HERE / "mechanics_T2_A.md",
    "C": HERE / "mechanics_T2_C_final.md",
    "E": HERE / "mechanics_T2_E_final.md",
}[ARM]
EXECUTOR = {
    "A": MVP1 / "runs" / "A" / "exec_request.py",
    "C": HERE / "exec_request_T2.py",
    "E": HERE / "exec_request_T2.py",
}[ARM]
GATED = ARM in ("C", "E")
TURNS = RUN / "turns"
LOG = RUN / "run.log"
SENT_MECH = None  # setup() 填充：实际发送的 mechanics 文本（D-015 cap 修复）


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def setup():
    """D-015 §4 BLOCKER 修复：cap 行窄正则改写（仅"共 15 轮上限"→
    "共 {CAP} 轮上限"）；快照 mechanics.txt = 实际发送文本（@15 与批准
    文件逐字节一致——CAP==15 时零改写直用原文；@30 含唯一改写行）；
    冻结批准文件本身零改动（只读）。"""
    if RUN.exists():
        shutil.rmtree(RUN)
    TURNS.mkdir(parents=True)
    shutil.copytree(FROZEN, RUN / "repo", symlinks=True)
    mech_text = MECH.read_text(encoding="utf-8")
    if CAP != 15:
        cap_pat = re.compile(r"共 15 轮上限")
        hits = cap_pat.findall(mech_text)
        assert len(hits) == 1, f"cap 行窄正则须恰命中 1 处，实际 {len(hits)}"
        mech_text = cap_pat.sub(f"共 {CAP} 轮上限", mech_text, count=1)
    (RUN / "mechanics.txt").write_text(mech_text, encoding="utf-8")
    global SENT_MECH
    SENT_MECH = mech_text
    log(f"setup T2 arm={ARM} repo=frozen 树 cap={CAP}"
        f"（mechanics 改写：{'无（@15 原文直用）' if CAP == 15 else 'cap 行→' + str(CAP)}）")


def call_model(prompt):
    mech = SENT_MECH  # 实际发送文本（含 cap 改写；快照=RUN/mechanics.txt）
    for attempt in range(1, 4):
        try:
            r = subprocess.run(
                ["bash", str(DS_AGENT), "-c", str(RUN / "conv.json"),
                 "-s", mech, prompt],
                capture_output=True, text=True, timeout=600, cwd=str(RUN))
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout
            log(f"API attempt {attempt} 失败 rc={r.returncode}: {r.stderr[-200:]}")
        except subprocess.TimeoutExpired:
            log(f"API attempt {attempt} 超时")
        time.sleep(10 * attempt)
    raise RuntimeError("API 连败 3 次——运行完整性事故")


def main():
    setup()
    tele = {"arm": f"T2-{ARM}", "task": "T2", "cap": CAP, "turns": [],
            "done_attempts": 0, "done_receipts": [], "outcome": None,
            "fdv": None, "cap_hit": False, "first_write": None,
            "turns_spent_before_first_write": None, "plan_attempts": 0,
            "plan_rejections": 0, "amendments": 0, "dsml_events": [],
            "self_report_parse": [], "new_test_files": [],
            "quote_clause": "gamma-D014", "truncation_events": 0}
    prompt = open(TASK, encoding="utf-8").read()
    done = False
    for t in range(1, CAP + 1):
        resp_path = TURNS / f"{t:02d}-response.md"
        fb_path = TURNS / f"{t:02d}-feedback.md"
        response = call_model(prompt)
        resp_path.write_text(response, encoding="utf-8")
        log(f"T{t}: response {len(response)}ch")
        env = dict(os.environ)
        if GATED:
            env["E_STATE"] = str(RUN / "state.json")
        ex = subprocess.run([sys.executable, str(EXECUTOR), str(resp_path),
                             str(fb_path)],
                            cwd=str(RUN / "repo"), env=env,
                            capture_output=True, text=True, timeout=600)
        summary = ex.stdout.strip()
        log(f"T{t}: exec rc={ex.returncode} {summary[:120]}")
        rec = {"t": t, "exec_rc": ex.returncode, "exec_summary": summary[:400]}
        if ex.returncode == 99:
            tele["done_attempts"] += 1
            ok, receipt, atel = run_acceptance(
                RUN / "repo", response, str(ACCEPT_CFG),
                snapshot_dir=str(RUN / "fdv-snapshots"))
            (RUN / f"acceptance-t{t}.json").write_text(
                json.dumps(atel, ensure_ascii=False, indent=1), encoding="utf-8")
            tele["done_receipts"].append({"t": t, "receipt": receipt})
            tele["self_report_parse"].append(
                {"t": t, "declarations": atel["self_report_details"],
                 "counts": atel["counts"]})
            if atel["new_test_files"]:
                tele["new_test_files"] = atel["new_test_files"]
            rec["receipt"] = receipt
            if ARM == "E":
                fb_path.write_text(receipt + "\n", encoding="utf-8")
                log(f"T{t}: DONE #{tele['done_attempts']} -> "
                    f"{receipt.splitlines()[0]}")
                if ok:
                    tele["outcome"] = "DONE_PASS"
                    tele["fdv"] = {"valid": True, "turn": t,
                                   "receipt": receipt, "counts": atel["counts"]}
                    tele["turns"].append(rec)
                    done = True
                    break
                tele["turns"].append(rec)
                prompt = fb_path.read_text(encoding="utf-8")
                continue
            else:
                fb_path.write_text(
                    "（运行已结束：DONE 收讫。验收为隐藏神谕离线判定，"
                    "结果不回填。）\n", encoding="utf-8")
                tele["outcome"] = "DONE_END"
                tele["fdv"] = {"valid": ok, "turn": t, "receipt": receipt,
                               "counts": atel["counts"]}
                log(f"T{t}: DONE -> 离线验收 {receipt.splitlines()[0]}")
                tele["turns"].append(rec)
                done = True
                break
        tele["turns"].append(rec)
        for w in re.findall(r"WRITE_OK (\S+)", summary):
            if tele["first_write"] is None:
                tele["first_write"] = w
                tele["turns_spent_before_first_write"] = t - 1
        if "PLAN_APPROVED" in summary:
            tele["plan_attempts"] += 1
        if "PLAN_REJECTED" in summary:
            tele["plan_rejections"] += 1
        if "畸形标记" in (fb_path.read_text(encoding="utf-8")
                       if fb_path.exists() else ""):
            tele["dsml_events"].append(t)
        if "WRITE_TRUNCATED" in summary:
            tele["truncation_events"] += 1  # D-015(2)：截断计数（分臂）
        prompt = fb_path.read_text(encoding="utf-8") if fb_path.exists() else ""
        if not prompt.strip():
            prompt = ("（未识别到工具请求。请发出 READ / RUN / WRITE 请求，"
                      "或单独一行 DONE。）")
    if not done:
        tele["cap_hit"] = True
        tele["outcome"] = "CAP" if tele["done_attempts"] == 0 else "DONE_FAIL_AT_CAP"
        if tele["fdv"] is None and tele["done_receipts"]:
            tele["fdv"] = {"valid": False,
                           "receipts": [r["receipt"] for r in tele["done_receipts"]]}
    (RUN / "telemetry.json").write_text(
        json.dumps(tele, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"END: outcome={tele['outcome']} done_attempts={tele['done_attempts']} "
        f"cap_hit={tele['cap_hit']}")


if __name__ == "__main__":
    main()
