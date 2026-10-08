"""INDEPENDENT_ACCEPTANCE 自测（D-005 自测覆盖要求）。

覆盖（块 10 Track 1d 指定）：
  1. DONE 触发路径（is_done_message 冻结正则 + CLI 端到端触发）
  2. 四行计数（spec/edge/存量/自报 的绿红与计数）
  3. PASS 边界含 n=0（纯 DONE、无声明 → 空真 PASS）
  4. 回执防泄露（回执=恰 5 行计数，无测试名/无神谕输出/无断言细节）

运行：cd <mvp1 根> && repo_frozen/.venv/bin/python -m pytest runs/E/test_independent_acceptance.py -v
（需 /tmp 可写；mock 仓库由 fixture 从 repo_frozen 复制构造）
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
MVP1_ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from independent_acceptance import (  # noqa: E402
    is_done_message, parse_self_reports, run_self_reports, run_acceptance)

SELFTEST_CFG = str(HERE / "selftest_config.json")
FROZEN = MVP1_ROOT / "repo_frozen"


@pytest.fixture(scope="module")
def repo_pass(tmp_path_factory):
    """PASS 路径 mock 仓库：冻结基线 + MARK。"""
    d = tmp_path_factory.mktemp("repo_pass")
    dst = d / "repo"
    shutil.copytree(FROZEN, dst, symlinks=True)
    (dst / "MARK").write_text("1")
    return dst


@pytest.fixture(scope="module")
def repo_fail(tmp_path_factory):
    """FAIL 路径 mock 仓库：冻结基线、无 MARK（spec 1/2）。"""
    d = tmp_path_factory.mktemp("repo_fail")
    dst = d / "repo"
    shutil.copytree(FROZEN, dst, symlinks=True)
    return dst


@pytest.fixture(scope="module")
def repo_newtest(tmp_path_factory):
    """存量破裂+新建测试文件 mock 仓库：MARK + 新增失败测试。"""
    d = tmp_path_factory.mktemp("repo_newtest")
    dst = d / "repo"
    shutil.copytree(FROZEN, dst, symlinks=True)
    (dst / "MARK").write_text("1")
    (dst / "tests" / "test_extra_new.py").write_text(
        "def test_extra_failing():\n    assert False, '构造的存量红点'\n")
    return dst


RECEIPT_PASS = ("ACCEPTANCE PASS\nspec-direct 2/2\nedge 1/1\n"
                "存量 28/28\n自报 0/0")
RECEIPT_FAIL_SPEC = ("ACCEPTANCE FAIL\nspec-direct 1/2\nedge 1/1\n"
                     "存量 28/28\n自报 0/0")


# ---------------- 1. DONE 触发路径 ----------------

def test_done_detection_frozen_regex():
    assert is_done_message("修复完成，全部验证通过。\nDONE\n")
    assert is_done_message("DONE")
    assert is_done_message("READ src/a.py\n\nDONE\n")  # 检测为纯函数；请求优先级属运行器
    assert not is_done_message("我会尽快 DONE，请稍候")
    assert not is_done_message("DONE 了")
    assert not is_done_message("DONE.")  # 行尾非空白字符→非单独一行
    assert not is_done_message("")


def test_cli_done_trigger_end_to_end(repo_pass, tmp_path):
    """CLI 路径：DONE 消息→验收→PASS 回执+退出码 0；非 DONE→rc=2 不触发。"""
    done_file = tmp_path / "done.md"
    done_file.write_text("任务完成。\nDONE\n", encoding="utf-8")
    env = {"MVP1_REPO": str(repo_pass)}
    r = subprocess.run(
        [sys.executable, str(HERE / "independent_acceptance.py"),
         SELFTEST_CFG, str(done_file)],
        cwd=str(MVP1_ROOT), env=env, capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stderr[-400:]
    assert r.stdout.strip() == RECEIPT_PASS
    not_done = tmp_path / "notdone.md"
    not_done.write_text("还在做，先跑个测试。\nRUN pytest tests/ -q", encoding="utf-8")
    r2 = subprocess.run(
        [sys.executable, str(HERE / "independent_acceptance.py"),
         SELFTEST_CFG, str(not_done)],
        cwd=str(MVP1_ROOT), env=env, capture_output=True, text=True, timeout=600)
    assert r2.returncode == 2 and "不触发" in r2.stdout


# ---------------- 2. 四行计数 ----------------

def test_four_line_counts_pass(repo_pass, tmp_path):
    ok, receipt, tel = run_acceptance(
        repo_pass, "DONE\n", SELFTEST_CFG, snapshot_dir=tmp_path / "snap")
    assert ok is True
    assert tel["counts"] == {"spec": [2, 2], "edge": [1, 1],
                             "existing": [28, 28], "self_reported": [0, 0]}


def test_four_line_counts_spec_red(repo_fail, tmp_path):
    ok, receipt, tel = run_acceptance(
        repo_fail, "DONE\n", SELFTEST_CFG, snapshot_dir=tmp_path / "snap")
    assert ok is False
    assert receipt == RECEIPT_FAIL_SPEC
    assert tel["counts"]["spec"] == [1, 2]
    assert tel["counts"]["existing"] == [28, 28]


def test_four_line_counts_existing_red_and_new_files(repo_newtest, tmp_path):
    ok, receipt, tel = run_acceptance(
        repo_newtest, "DONE\n", SELFTEST_CFG, snapshot_dir=tmp_path / "snap")
    assert ok is False
    assert "存量 28/29" in receipt
    assert tel["counts"]["existing"] == [28, 29]
    # 5.2(c)：未声明新建测试文件 → 遥测"新建测试文件数 vs 声明数"
    assert tel["new_test_files"] == ["test_extra_new.py"]
    assert tel["new_test_files_vs_declared"] == [1, 0]


# ---------------- 3. PASS 边界（含 n=0）与自报执行器 ----------------

def test_self_reports_stub_is_n0():
    """5.2(d)：冻结 DONE 格式无声明槽位 → 恒 n=0（不自行约定口径）。"""
    text = "完成。我跑了 pytest tests/ -q 全绿，还加了 test_foo.py。\nDONE\n"
    assert parse_self_reports(text) == []


def test_self_report_executor_pass_fail_error(repo_pass):
    """执行器单元：w 计通过（rc=0）；失败与执行报错计入 n 不计入 w。"""
    w, details = run_self_reports(
        repo_pass, ["true", "false", "definitely_missing_cmd_xyz"])
    assert w == 1 and len(details) == 3
    assert [d["passed"] for d in details] == [True, False, False]
    # 执行报错（127）与失败（1）都计入 n 不计入 w
    assert details[2]["rc"] == 127


def test_pass_boundary_n0_vacuous(repo_pass, tmp_path):
    """D-005 5.3：n=0 合法空真，不阻 PASS（纯 DONE 消息）。"""
    ok, receipt, _ = run_acceptance(
        repo_pass, "DONE\n", SELFTEST_CFG, snapshot_dir=tmp_path / "snap")
    assert ok is True and "自报 0/0" in receipt


def test_integrity_fuse_on_config_mismatch(repo_pass, tmp_path):
    """D-004(4) 熔断口径：神谕结果集与配置清单不重合 → RuntimeError。"""
    bad = json.loads(Path(SELFTEST_CFG).read_text())
    bad["spec_tests"] = ["test_mock_spec_always", "test_mock_nonexistent"]
    bad_path = tmp_path / "bad_config.json"
    bad_path.write_text(json.dumps(bad))
    with pytest.raises(RuntimeError, match="不重合"):
        run_acceptance(repo_pass, "DONE\n", str(bad_path),
                       snapshot_dir=tmp_path / "snap")


# ---------------- 4. 回执防泄露 ----------------

LEAK_MARKERS = ["test_mock", "test_", "MARK", "pytest", "passed",
                "assert", "Traceback", "spec_notes", "oracle"]


@pytest.mark.parametrize("case", ["pass", "spec_red", "existing_red"])
def test_receipt_anti_leak(case, repo_pass, repo_fail, repo_newtest, tmp_path):
    """防泄露（D-005 已知局限条款）：回执只含四行计数——无测试名、无神谕
    输出、无断言细节；恰 5 行；2-5 行均为 计数 行。"""
    repo = {"pass": repo_pass, "spec_red": repo_fail,
            "existing_red": repo_newtest}[case]
    ok, receipt, _ = run_acceptance(
        repo, "DONE\n", SELFTEST_CFG, snapshot_dir=tmp_path / "snap")
    lines = receipt.splitlines()
    assert len(lines) == 5, receipt
    assert lines[0] in ("ACCEPTANCE PASS", "ACCEPTANCE FAIL")
    for line in lines[1:]:
        m = re.match(r"^(\S[^/]*\S|\S) (\d+)/(\d+)$", line)
        assert m, "计数行格式异常：%r" % line
        assert int(m.group(2)) <= int(m.group(3)), line
    # 防泄露标记扫描（回执是 agent 可见物，任何神谕细节都不允许出现）
    for marker in LEAK_MARKERS:
        assert marker not in receipt, (marker, receipt)
    # 回执与遥测隔离：遥测才含 per-test 细节，回执绝无


def test_fdv_snapshot_created(repo_pass, tmp_path):
    ok, _, tel = run_acceptance(
        repo_pass, "DONE\n", SELFTEST_CFG, snapshot_dir=tmp_path / "snap")
    snap = Path(tel["integrity"]["snapshot"])
    assert snap.exists() and snap.stat().st_size > 0
    assert tel["integrity"]["errors"] == []


# ---------------- D-007：TEST 声明语法（2026-10-09 05:10 裁决落地） ----------------

def test_d007_zero_declarations():
    """零声明类：正文提及测试但无 TEST 行 → n=0（D-007(3)）。"""
    msg = "完成。我自测了 pytest tests/ -q 全绿，还加了两个测试文件。\nDONE\n"
    assert parse_self_reports(msg) == []
    assert parse_self_reports("DONE\n") == []


def test_d007_multiple_and_duplicate_declarations():
    """多条声明类：DONE 行后多条、不紧邻、重复各计一次（D-007(1)(2)）。"""
    msg = ("实现完成。\nDONE\n"
           "TEST .venv/bin/python -m pytest tests/test_a.py -q\n"
           "中间说明文字，不是声明\n"
           "TEST .venv/bin/python -m pytest tests/test_a.py -q\n"
           "TEST tests/test_b.py\n")
    assert parse_self_reports(msg) == [
        ".venv/bin/python -m pytest tests/test_a.py -q",
        ".venv/bin/python -m pytest tests/test_a.py -q",
        "tests/test_b.py"]


def test_d007_prefix_variants_not_declared():
    """前缀变体类：小写 test / 裸 TEST / 行首空白 / DONE 行之前 → 均非声明
    （D-007(3) 精确前缀）。"""
    msg = ("test pytest tests/x.py\n"
           "TEST\n"
           "   TEST tests/y.py\n"
           "TESTtests/z.py\n"
           "DONE\n"
           "test pytest tests/w.py\n")
    assert parse_self_reports(msg) == []


def test_d007_error_declaration_n_not_w(repo_pass):
    """含错声明类：执行报错/文件不存在 → 计 n 不计 w（D-007(2) 5.2(b)）。"""
    w, details = run_self_reports(
        repo_pass, ["tests/definitely_missing.py", "exit 7"])
    assert w == 0 and len(details) == 2
    assert all(d["passed"] is False for d in details)


def test_d007_path_form_pytest_execution(repo_pass, tmp_path):
    """路径形态：repo 内存在且 .py → venv pytest 执行（D-007 命令或测试
    路径）；新建通过测试 → w=1。"""
    import shutil as _sh
    dst = tmp_path / "repo_pathform"
    _sh.copytree(repo_pass, dst)
    (dst / "tests" / "test_declared_new.py").write_text(
        "def test_ok():\n    assert 1 + 1 == 2\n")
    w, details = run_self_reports(dst, ["tests/test_declared_new.py"])
    assert w == 1, details
    assert details[0]["form"] == "pytest-path"
    w2, _ = run_self_reports(dst, [".venv/bin/python -m pytest tests/test_declared_new.py -q"])
    assert w2 == 1  # 命令形态同过


def test_d007_integration_receipt_self_report_line(repo_pass, tmp_path):
    """集成：DONE + TEST 声明（通过）→ 回执自报 1/1 且 PASS；声明失败 →
    自报 0/1 且 FAIL（w≠n 阻断，D-005 5.3）。"""
    import shutil as _sh
    dst = tmp_path / "repo_d007_int"
    _sh.copytree(repo_pass, dst)
    (dst / "tests" / "test_declared_ok.py").write_text(
        "def test_ok():\n    assert True\n")
    ok, receipt, tel = run_acceptance(
        dst, "DONE\nTEST tests/test_declared_ok.py\n",
        SELFTEST_CFG, snapshot_dir=tmp_path / "snap")
    assert ok is True and "自报 1/1" in receipt
    assert tel["new_test_files"] == ["test_declared_ok.py"]
    assert tel["new_test_files_vs_declared"] == [1, 1]
    bad, receipt2, _ = run_acceptance(
        dst, "DONE\nTEST tests/definitely_missing.py\n",
        SELFTEST_CFG, snapshot_dir=tmp_path / "snap")
    assert bad is False and "自报 0/1" in receipt2
