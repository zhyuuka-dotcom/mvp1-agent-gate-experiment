#!/usr/bin/env python3
"""E@15 循环驱动器（E 放行 2026-10-09 06:30，运行纪律见指令 §5）。

流程：repo=污染修复版树（repo_frozen 内容，即 6ad0f5e 冻结树）→
mechanics=批准原文（system）+ task.md（首条 user）→ 逐轮：ds-agent
（flash/2048/思考关，A/C 同款）→ turns/tN-response.md → exec_request_e
（cwd=repo）→ 回执回填 → DONE(exit99) → INDEPENDENT_ACCEPTANCE →
四行回执即该轮回填；PASS→运行结束（FDV 真）；FAIL→继续；15 轮 cap。
零干预：仅事故（API 连败/执行器异常）中止-归档-留痕-待修复重跑。

用法: E_STATE 无需设（默认 run_root/state.json）
      python3 run_e.py [run_root=/tmp/e15] [cap=15]
输出: run_root/{turns,conv.json,state.json,telemetry.json,run.log}
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
LEARNHUB = MVP1.parent.parent  # /home/z/my-project/learnhub
DS_AGENT = LEARNHUB / "bin" / "ds-agent.sh"
FROZEN = MVP1 / "repo_frozen"
MECHANICS = HERE / "mechanics_e_draft.md"
TASK = MVP1 / "tasks" / "T1" / "task.md"
ACCEPT_CFG = HERE / "acceptance_config_T1.json"

sys.path.insert(0, str(HERE))
from independent_acceptance import run_acceptance  # noqa: E402

RUN = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/e15").resolve()
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 15
REPO = RUN / "repo"
TURNS = RUN / "turns"
LOG = RUN / "run.log"


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def setup():
    if RUN.exists():
        shutil.rmtree(RUN)
    TURNS.mkdir(parents=True)
    shutil.copytree(FROZEN, REPO, symlinks=True)
    shutil.copy(MECHANICS, RUN / "mechanics.txt")  # §1 运行文本快照入运行记录
    log(f"setup: repo=repo_frozen 树（污染修复版/6ad0f5e 冻结树）, cap={CAP}")


def call_model(prompt, is_first):
    """ds-agent 调用（A/C 同款参数）；返回 response 文本。连败 3 次=事故。"""
    mech = open(MECHANICS, encoding="utf-8").read()
    for attempt in range(1, 4):
        try:
            r = subprocess.run(
                ["bash", str(DS_AGENT), "-c", str(RUN / "conv.json"),
                 "-s", mech, prompt],
                capture_output=True, text=True, timeout=600, cwd=str(RUN))
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout, r.stderr
            log(f"API attempt {attempt} 失败 rc={r.returncode}: {r.stderr[-200:]}")
        except subprocess.TimeoutExpired:
            log(f"API attempt {attempt} 超时（600s）")
        time.sleep(10 * attempt)
    raise RuntimeError("API 连败 3 次——运行完整性事故")


def usage_tail():
    try:
        with open(LEARNHUB / "logs" / "ds-usage.tsv", encoding="utf-8") as f:
            return f.read().strip().splitlines()[-1]
    except Exception:
        return ""


def main():
    setup()
    tele = {
        "arm": "E", "task": "T1", "cap": CAP, "turns": [], "done_attempts": 0,
        "done_receipts": [], "outcome": None, "fdv": None, "cap_hit": False,
        "turns_spent_before_first_write": None, "first_write": None,
        "plan_attempts": 0, "plan_rejections": 0, "amendments": 0,
        "dsml_events": [], "self_report_parse": [], "new_test_files": [],
        "usage_rows": [],
    }
    task_text = open(TASK, encoding="utf-8").read()
    prompt = task_text  # T1 首条消息（A/C 同构：system=mechanics, user=task）
    done = False
    for t in range(1, CAP + 1):
        resp_path = TURNS / f"{t:02d}-response.md"
        fb_path = TURNS / f"{t:02d}-feedback.md"
        response, meta = call_model(prompt, t == 1)
        tele["usage_rows"].append(usage_tail())
        resp_path.write_text(response, encoding="utf-8")
        log(f"T{t}: response {len(response)}ch saved")
        # 执行（cwd=repo；E_STATE=run_root/state.json）
        env = dict(os.environ, E_STATE=str(RUN / "state.json"))
        ex = subprocess.run(
            [sys.executable, str(HERE / "exec_request_e.py"),
             str(resp_path), str(fb_path)],
            cwd=str(REPO), env=env, capture_output=True, text=True, timeout=600)
        exec_summary = ex.stdout.strip()
        log(f"T{t}: exec rc={ex.returncode} {exec_summary[:120]}")
        turn_rec = {"t": t, "exec_rc": ex.returncode,
                    "exec_summary": exec_summary[:400]}
        if ex.returncode == 99:
            # DONE → INDEPENDENT_ACCEPTANCE（四行回执即回填；PASS→终）
            tele["done_attempts"] += 1
            try:
                ok, receipt, atel = run_acceptance(
                    REPO, response, str(ACCEPT_CFG),
                    snapshot_dir=str(RUN / "fdv-snapshots"))
            except Exception as e:
                log(f"T{t}: 验收完整性事故: {e!r}")
                raise
            fb_path.write_text(receipt + "\n", encoding="utf-8")
            (RUN / f"acceptance-t{t}.json").write_text(
                json.dumps(atel, ensure_ascii=False, indent=1), encoding="utf-8")
            tele["done_receipts"].append({"t": t, "receipt": receipt})
            tele["self_report_parse"].append(
                {"t": t, "declarations": atel["self_report_details"],
                 "counts": atel["counts"]})
            if atel["new_test_files"]:
                tele["new_test_files"] = atel["new_test_files"]
            turn_rec["receipt"] = receipt
            log(f"T{t}: DONE #{tele['done_attempts']} -> {receipt.splitlines()[0]}")
            if ok:
                tele["outcome"] = "DONE_PASS"
                tele["fdv"] = {"valid": True, "turn": t,
                               "receipt": receipt,
                               "counts": atel["counts"]}
                tele["turns"].append(turn_rec)
                done = True
                break
            tele["turns"].append(turn_rec)
            prompt = fb_path.read_text(encoding="utf-8")
            continue
        # 正常轮/空转轮：反馈即下轮 prompt
        tele["turns"].append(turn_rec)
        # 遥测派生
        for code in re.findall(r"WRITE_OK (\S+)", exec_summary):
            if tele["first_write"] is None:
                tele["first_write"] = code
                tele["turns_spent_before_first_write"] = t - 1
        if "PLAN_APPROVED" in exec_summary:
            tele["plan_attempts"] += 1
        if "PLAN_REJECTED" in exec_summary:
            tele["plan_rejections"] += 1
        if "畸形标记" in open(fb_path, encoding="utf-8").read():
            tele["dsml_events"].append(t)
        prompt = fb_path.read_text(encoding="utf-8")
        if not prompt.strip():
            prompt = "（未识别到工具请求。请发出 READ / RUN / WRITE 请求，或单独一行 DONE。）"
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
