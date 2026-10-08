#!/usr/bin/env python3
"""第二轮@30 通用驱动器（D-001-增补(1) 自动启动；A/C/E 三臂）。

臂差异：
  A30：executor=runs/A/exec_request.py（无门禁）；DONE→离线验收（回执
        仅入遥测，不回填 agent）→运行结束
  C30：executor=exec_request_e.py（PLAN 门禁；E_STATE 指本 run）；
        DONE→离线验收→结束
  E30：executor=exec_request_e.py；DONE→INDEPENDENT_ACCEPTANCE→四行
        回执回填→继续（PASS→结束；FAIL→循环至 cap）
运行纪律与 run_e.py 相同（flash/2048/思考关/零干预/事故中止-归档-重跑）。
mechanics：第一轮冻结文本仅改 cap 15→30（预算继承 D-004(8)：不衰减）。

用法: python3 run_arm.py <A30|C30|E30> [run_root=/tmp/<arm>]
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
MVP1 = HERE.parent
LEARNHUB = MVP1.parent.parent
DS_AGENT = LEARNHUB / "bin" / "ds-agent.sh"
FROZEN = MVP1 / "repo_frozen"
TASK = MVP1 / "tasks" / "T1" / "task.md"
ACCEPT_CFG = HERE / "E" / "acceptance_config_T1.json"

sys.path.insert(0, str(HERE / "E"))
from independent_acceptance import run_acceptance  # noqa: E402

ARM = sys.argv[1] if len(sys.argv) > 1 else "E30"
RUN = Path(sys.argv[2] if len(sys.argv) > 2 else f"/tmp/{ARM.lower()}").resolve()
CAP = 30
MECH = HERE / ARM / "mechanics.txt"
if ARM == "A30":
    EXECUTOR = HERE / "A" / "exec_request.py"
    GATED = False
elif ARM in ("C30", "E30"):
    EXECUTOR = HERE / "E" / "exec_request_e.py"
    GATED = True
else:
    raise SystemExit(f"未知臂 {ARM}")
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
    shutil.copytree(FROZEN, RUN / "repo", symlinks=True)
    shutil.copy(MECH, RUN / "mechanics.txt")
    log(f"setup arm={ARM} repo=frozen 树 cap={CAP}")


def call_model(prompt):
    mech = open(MECH, encoding="utf-8").read()
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
    tele = {"arm": ARM, "task": "T1", "round": 2, "cap": CAP, "turns": [],
            "done_attempts": 0, "done_receipts": [], "outcome": None,
            "fdv": None, "cap_hit": False, "first_write": None,
            "turns_spent_before_first_write": None, "plan_attempts": 0,
            "plan_rejections": 0, "amendments": 0, "dsml_events": [],
            "self_report_parse": [], "new_test_files": []}
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
            if ARM == "E30":
                # E：回执回填，FAIL 继续，PASS 结束
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
                # A/C：离线验收（回执只入遥测，不给 agent），运行结束
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
