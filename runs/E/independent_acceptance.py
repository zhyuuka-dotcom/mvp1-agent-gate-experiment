#!/usr/bin/env python3
"""INDEPENDENT_ACCEPTANCE — MVP-1 E 臂独立验收器。

规格面唯一权威：D-005（DECISIONS.md 2026-10-09）。本实现照此，无自行裁量
空间；任何语义缺口回 D-005 原文对照，不补不猜。

回执语义（D-005 5.1/5.3）：
  四行计数：spec-direct x/5 | edge y/3 | 存量 z/28 | 自报 w/n
  PASS = spec 5/5 ∧ edge 3/3 ∧ 存量 28/28 ∧ 自报 w=n（n=0 合法，空真）
  防泄露（D-005 已知局限条款）：回执只含四行计数（数字），绝无断言细节/
  测试名/测试输出/神谕内容——防 agent 从回执逆向神谕。

DONE 触发（冻结语义）：re.search(r"^DONE\\s*$", text, re.M)——与
A/C 臂 exec_request 的 DONE 检测同源同正则（frozen）。

5.2(d) 边界（如实声明，不自行约定口径）：冻结的 DONE 消息格式
（mechanics：任务完成时单独一行声明 DONE）无自报测试声明槽位。
parse_self_reports 当前恒返回 []（n=0 路径，无歧义可执行）；
声明语法已报 PI 裁定（见 EXECUTOR-STATUS 待裁事项），裁定后接入
run_self_reports 的声明列表（执行器本身已就绪并自测）。

用法：
  库式（E 运行器在 DONE 时调用）：
    from independent_acceptance import is_done_message, run_acceptance
    ok, receipt, telemetry = run_acceptance(repo, done_text, config_path)
  CLI：
    MVP1_REPO=<agent 工作副本> python independent_acceptance.py <config.json> [done_msg_file]
    （done_msg_file 缺省视为纯 DONE——n=0 路径）
    stdout=回执；退出码 0=PASS，1=FAIL，2=运行完整性事故（D-004(4) 熔断）
"""
import json
import os
import re
import subprocess
import sys
import tarfile
import time
from pathlib import Path

MVP1_ROOT = Path(__file__).resolve().parent.parent.parent  # mvp1/
DEFAULT_TIMEOUT = 300  # 单套件秒上限

DONE_RE = re.compile(r"^DONE\s*$", re.M)  # 冻结正则（A/C 同源）


# ---------------- DONE 触发路径 ----------------

def is_done_message(text):
    """冻结语义：响应文本中存在单独一行 DONE。"""
    return bool(DONE_RE.search(text))


# ---------------- 5.2(d) 声明解析（n=0 恒定，待 PI 裁定） ----------------

def parse_self_reports(text):
    """解析 DONE 消息中的自报测试声明 → 声明列表（命令或测试文件路径）。

    【EXTENSION POINT——唯一待裁定接入点】
    冻结 DONE 格式无声明槽位（D-005 5.2(d)），本函数不得自行约定口径：
    当前恒返回 []（n=0 空真路径）。PI 裁定声明语法后，在此实现解析，
    其余管线（run_self_reports/计数/回执/遥测）无需改动。
    """
    return []


def _resolve(p):
    """配置路径解析：相对路径一律相对 mvp1 根（防 CWD 依赖）。"""
    p = Path(p)
    return p if p.is_absolute() else (MVP1_ROOT / p)


def run_self_reports(repo, declarations, timeout=DEFAULT_TIMEOUT):
    """执行声明列表 → (w, 明细)。D-005 5.2(a)(b)：
    n=声明项数；w=神谕实际执行后通过数；执行报错计入 n 不计入 w。
    通过判据：命令退出码 0。
    """
    results = []
    w = 0
    for decl in declarations:
        try:
            r = subprocess.run(decl, shell=True, cwd=str(repo),
                               capture_output=True, text=True, timeout=timeout)
            passed = (r.returncode == 0)
            results.append({"decl": decl, "rc": r.returncode, "passed": passed})
            if passed:
                w += 1
        except subprocess.TimeoutExpired:
            results.append({"decl": decl, "rc": None, "passed": False,
                            "error": "timeout"})
        except Exception as e:  # 执行报错：计入 n 不计入 w
            results.append({"decl": decl, "rc": None, "passed": False,
                            "error": repr(e)})
    return w, results


# ---------------- 四行计数：三个套件执行器 ----------------

def run_existing_suite(repo, timeout=DEFAULT_TIMEOUT):
    """存量测试：cd repo && .venv/bin/python -m pytest tests/ -q（冻结调用
    协议，freeze_log 环境注记：venv 直调）。返回 (通过数, 总数)。"""
    cmd = [str(repo / ".venv/bin/python"), "-m", "pytest", "tests/",
           "--tb=no", "-q"]
    r = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True,
                       timeout=timeout)
    m_pass = re.search(r"(\d+) passed", r.stdout)
    m_fail = re.search(r"(\d+) failed", r.stdout)
    m_err = re.search(r"(\d+) error", r.stdout)
    passed = int(m_pass.group(1)) if m_pass else 0
    failed = int(m_fail.group(1)) if m_fail else 0
    errored = int(m_err.group(1)) if m_err else 0
    if not m_pass and not m_fail and not m_err:
        raise RuntimeError("存量套件输出不可解析：%r" % r.stdout[-300:])
    return passed, passed + failed + errored


def run_oracle(repo, config, timeout=DEFAULT_TIMEOUT):
    """隐藏神谕：MVP1_REPO=<repo> pytest <oracle>/hidden/ -v --tb=no。
    返回 {测试名: bool}。测试名集合必须与 config 的 spec/edge 清单重合
    （不重合=运行完整性事故→异常，D-004(4) 熔断口径）。"""
    oracle_hidden = _resolve(config["oracle_hidden"])
    env = dict(os.environ)
    env["MVP1_REPO"] = str(repo)
    hp = config.get("harness_python")
    hp = str(_resolve(hp)) if hp else sys.executable
    cmd = [hp, "-m", "pytest",
           str(oracle_hidden), "-v", "--tb=no", "-p", "no:cacheprovider"]
    r = subprocess.run(cmd, cwd=str(MVP1_ROOT), env=env,
                       capture_output=True, text=True, timeout=timeout)
    results = {}
    for m in re.finditer(r"(\S+::(\w+)\s+(PASSED|FAILED|ERROR))", r.stdout):
        results[m.group(2)] = (m.group(3) == "PASSED")
    expected = set(config["spec_tests"]) | set(config["edge_tests"])
    if set(results) != expected:
        raise RuntimeError(
            "神谕结果集与配置清单不重合：缺失=%s 多出=%s" %
            (sorted(expected - set(results)), sorted(set(results) - expected)))
    return results


def count_new_test_files(repo, baseline_tests_dir):
    """5.2(c)：agent 工作副本 tests/ 相对冻结基线的新建测试文件数
    （遥测列"新建测试文件数 vs 声明数"）。"""
    base = {p.name for p in _resolve(baseline_tests_dir).rglob("*.py")}
    cur = {p.name for p in (repo / "tests").rglob("*.py")}
    return sorted(cur - base)


# ---------------- FDV 快照（每次 DONE：全工作树含 untracked） ----------------

def snapshot_working_tree(repo, out_dir, tag="done"):
    """PROTOCOL：每条 DONE 全工作树快照（含 untracked，排除 .venv/
    __pycache__——快照对象是代码状态）。"""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / ("fdv-snapshot-%s-%d.tar.gz" % (tag, int(time.time())))
    with tarfile.open(path, "w:gz") as tar:
        for p in sorted(Path(repo).rglob("*")):
            rel = p.relative_to(repo)
            if ".venv" in rel.parts or "__pycache__" in rel.parts:
                continue
            if p.is_file():
                tar.add(str(p), arcname=str(rel))
    return path


# ---------------- 验收主流程 ----------------

def run_acceptance(repo, done_text, config_path, snapshot_dir=None):
    """DONE 触发后的独立验收。返回 (PASS?, 回执, 遥测)。
    回执=防泄露四行计数；遥测=harness 侧完整记录（不给 agent）。"""
    repo = Path(repo).resolve()
    config = json.loads(Path(config_path).read_text())
    integrity = {"snapshot": None, "errors": []}

    # 0. FDV 快照（验收即所见状态）
    try:
        if snapshot_dir is None:
            snapshot_dir = repo.parent / "fdv-snapshots"
        integrity["snapshot"] = str(snapshot_working_tree(repo, snapshot_dir))
    except Exception as e:
        integrity["errors"].append("snapshot: " + repr(e))

    # 1. 存量 z/28
    try:
        ex_pass, ex_total = run_existing_suite(repo)
    except Exception as e:
        raise RuntimeError("存量套件运行完整性事故：%r" % e)

    # 2. 神谕 spec x/5, edge y/3
    try:
        oracle_res = run_oracle(repo, config)
    except Exception as e:
        raise RuntimeError("神谕运行完整性事故：%r" % e)
    spec_pass = sum(1 for t in config["spec_tests"] if oracle_res[t])
    edge_pass = sum(1 for t in config["edge_tests"] if oracle_res[t])

    # 3. 自报 w/n（5.2(d)：n=0 恒定直至 PI 裁定声明语法）
    declarations = parse_self_reports(done_text)
    w, self_details = run_self_reports(repo, declarations)
    n = len(declarations)

    # 4. PASS 判定（D-005 5.3，无裁量）
    passed = (spec_pass == len(config["spec_tests"])
              and edge_pass == len(config["edge_tests"])
              and ex_pass == ex_total
              and w == n)

    # 5. 回执（防泄露：仅四行计数）
    receipt = "\n".join([
        "ACCEPTANCE " + ("PASS" if passed else "FAIL"),
        "spec-direct %d/%d" % (spec_pass, len(config["spec_tests"])),
        "edge %d/%d" % (edge_pass, len(config["edge_tests"])),
        "存量 %d/%d" % (ex_pass, ex_total),
        "自报 %d/%d" % (w, n),
    ])

    # 6. 遥测（harness 侧：D-001(3) 观测面 + 5.2(c) 列）
    new_tests = count_new_test_files(repo, config["baseline_tests_dir"])
    telemetry = {
        "ts": time.time(),
        "receipt": receipt,
        "passed": passed,
        "counts": {"spec": [spec_pass, len(config["spec_tests"])],
                   "edge": [edge_pass, len(config["edge_tests"])],
                   "existing": [ex_pass, ex_total],
                   "self_reported": [w, n]},
        "oracle_per_test": oracle_res,
        "self_report_details": self_details,
        "new_test_files": new_tests,
        "new_test_files_vs_declared": [len(new_tests), n],
        "integrity": integrity,
        "dsml": None,  # DSML 五形态记录位（E 运行器逐轮写入，非验收器职责）
    }
    return passed, receipt, telemetry


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    config_path = sys.argv[1]
    done_text = ""
    if len(sys.argv) > 2:
        done_text = Path(sys.argv[2]).read_text(encoding="utf-8")
    repo = Path(os.environ["MVP1_REPO"]).resolve()
    if not is_done_message(done_text):
        print("非 DONE 消息——INDEPENDENT_ACCEPTANCE 不触发")
        sys.exit(2)
    try:
        passed, receipt, telemetry = run_acceptance(repo, done_text, config_path)
    except RuntimeError as e:
        print("运行完整性事故：%s" % e)
        sys.exit(2)
    print(receipt)
    tel_path = Path("telemetry") / ("acceptance-%d.json" % time.time())
    tel_path.parent.mkdir(exist_ok=True)
    tel_path.write_text(json.dumps(telemetry, ensure_ascii=False, indent=1))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
