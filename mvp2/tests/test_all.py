"""WP-1 阶段 2｜自测（零 agent 运行，D-021 §5）

(a) 计数器与状态机全路径
(b) 固定回执内容不变性（任意隐藏失败组合下逐字节相同）
(c) 反馈生成器泄漏性质测试（种子失败注入：类别映射正确+无泄漏）
(d) MULTI_REQ 检测回归——MVP-1 的 84+1 命中语料为 ground truth
    （V32 报告表；runs/V32-multi-request-scan.md）
    **已知差异登记**：C 臂 3 处 DSML 多请求为 V32 扫描器漏检
    （本检测器检出、V32 未计；详见 WP1-REPORT §d）——测试将其
    固定为精确差异集，防未来新差异静默溜入。
(e) audit-error 分类测试（含存疑从宽路径）
(f) 覆盖表生成与不可见性验证

运行：python -m pytest mvp2/tests/test_all.py -q
（零 agent 运行——不调用任何 API）
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
MVP1_ROOT = HERE.parent.parent          # lab/mvp1/
sys.path.insert(0, str(MVP1_ROOT))

from mvp2.budget import BudgetError, BudgetState, Phase  # noqa: E402
from mvp2.constants import FIXED_RECEIPT_TEXT  # noqa: E402
from mvp2.fixed_receipt import _Sanitizer, fixed_receipt  # noqa: E402
from mvp2.feedback import FeedbackValueError, render_feedback  # noqa: E402
from mvp2.hidden_corpus import DRAFT_CORPUS  # noqa: E402
from mvp2.multireq import analyze  # noqa: E402
from mvp2.audit_error import (  # noqa: E402
    ambiguous_to_audit_error, classify_input_incomplete,
    classify_oracle_timeout, classify_selftest_fail, record_event,
)
from mvp2.coverage import DRAFT_TABLE  # noqa: E402
from mvp2.calibration import evaluate_dual_band, replacement_rule  # noqa: E402


# ── (a) 计数器与状态机全路径 ─────────────────────────────────────

def test_budget_full_paths():
    # D 路径（门+审计全开｜D）：29 工作轮 + 第 30 轮 DONE 声明
    # （DONE 轮计入 N——T3-A@30 末轮 DONE 先例）
    b = BudgetState(arm="D")
    for i in range(29):
        ok = b.consume_work()
    assert b.phase is Phase.WORKING and b.n_used == 29
    b.declare_done()                     # D：门开 → DONE_DECLARED（n_used=30）
    assert b.phase is Phase.DONE_DECLARED and b.n_used == 30
    b.accept_feedback()                  # 验收失败 → FEEDBACK（扣 F）
    assert b.f_used == 1 and b.repairs_started
    for i in range(5):
        b.consume_repair()               # M 修复轮
    assert b.m_used == 5 and b.m_exhausted_unverified()
    with pytest.raises(BudgetError):
        b.consume_repair()               # M 已耗尽不得再启动
    b.finalize("failed-unverified")
    assert b.phase.value == "failed-unverified"   # S6 交付三态字符串
    assert b.phase.is_terminal

    # A/B 路径（终态审计关 → CAP）
    a = BudgetState(arm="A")
    for i in range(30):
        a.consume_work()
    assert a.phase is Phase.CAP          # A：N 耗尽且审计关 → T=0 硬终止
    a2 = BudgetState(arm="A")
    a2.declare_done()                    # A：门关 → 不触发（仍离线测量）
    assert a2.phase is Phase.WORKING     # 预算面零变化
    with pytest.raises(BudgetError):
        a.consume_work()                 # CAP 后不得再消耗

    # B 路径：F 耗尽 → 固定回执
    b2 = BudgetState(arm="B")
    for i in range(29):
        b2.consume_work()
    b2.declare_done()
    for i in range(5):
        b2.accept_feedback()
    assert b2.f_used == 5
    with pytest.raises(BudgetError):
        b2.accept_feedback()             # F 耗尽 → 驱动器注入 FIXED_RECEIPT

    # audit-error 三不 + 单次重跑
    b3 = BudgetState(arm="B")
    b3.consume_work()
    snap_before = (b3.n_used, b3.m_used, b3.f_used)
    b3.register_audit_error("ORACLETIMEOUT")
    assert (b3.n_used, b3.m_used, b3.f_used) == snap_before   # 不扣预算
    assert b3.rerun_flag and not b3.phase.is_terminal         # 允许一次重跑
    b3.register_audit_error("ORACLEEXCEPTION")
    assert b3.phase is Phase.AUDIT_ERROR   # 第二次 → 终局 audit-error
    with pytest.raises(BudgetError):
        b3.register_audit_error("NOT-A-CODE")  # 四类外原因码拒绝


# ── (b) 固定回执内容不变性 ────────────────────────────────────────

def test_fixed_receipt_byte_invariance():
    b = BudgetState(arm="B")
    for i in range(29):
        b.consume_work()
    b.declare_done()
    for i in range(5):
        b.accept_feedback()
    # 任意隐藏失败组合（类别/次数/观测值变化）下逐字节相同：
    scenarios = [
        {"cats": ["EC-1"], "fails": 3, "obs": "assert 6.0 != 5.0"},
        {"cats": ["EC-1", "EC-2", "EC-3"], "fails": 17, "obs": "traceback..."},
        {"cats": [], "fails": 0, "obs": ""},
    ]
    receipts = {fixed_receipt(b) for _ in scenarios}
    assert receipts == {FIXED_RECEIPT_TEXT}      # 单一逐字节形态
    # 零动态信息守卫
    assert _Sanitizer.check_invariance() is True


# ── (c) 反馈生成器泄漏性质测试 ────────────────────────────────────

def test_feedback_leak_properties():
    b = BudgetState(arm="B")
    for i in range(29):
        b.consume_work()
    b.declare_done()
    b.accept_feedback()
    # 种子失败注入（正确路径）：类别句柄 → 白名单渲染
    out = render_feedback(b, {"EC-2", "EC-1"})
    assert "EC-1" in out and "EC-2" in out
    assert "EC-3" not in out                    # 未失败类别不出现（去重/选择规则）
    # 剩余额度字段（M/F 数字来自状态机——这是协议信息，允许且必须）
    assert "剩余修复轮 5" in out and "剩余反馈额度 4" in out
    # 泄漏性质：类别内部描述（映射表值）不得出现在 agent 可见反馈
    for leaked in DRAFT_CORPUS.mapping.values():
        assert leaked not in out
    # 白名单外取值 → 构造期拒绝（执行器无诊断生成权）
    with pytest.raises(FeedbackValueError):
        render_feedback(b, {"NOT-A-HANDLE"})
    with pytest.raises(FeedbackValueError):
        render_feedback(b, {"EC-999"})          # 未冻结句柄


# ── (d) MULTI_REQ 检测回归（84+1 语料 ground truth） ───────────────

# V32 报告 §1 表（期望命中数）；T1 第一轮目录名无任务前缀
V32_TRUTH = {
    "runs/A": 1, "runs/C": 0, "runs/E": 9,
    "runs/A30": 0, "runs/C30": 0, "runs/E30": 16,
    "runs/T2/A15": 0, "runs/T2/C15": 0, "runs/T2/E15": 13,
    "runs/T2/A30": 0, "runs/T2/C30": 0, "runs/T2/E30": 29,
    "runs/T3/A15": 0, "runs/T3/C15": 0, "runs/T3/E15": 0,
    "runs/T3/A30": 0, "runs/T3/C30": 0, "runs/T3/E30": 17,
}
# 已知差异：V32 扫描器对 C 臂 DSML 多请求（同消息双 invoke / 双
# calls 块）漏检 3 处——本检测器（按"每次回复恰好一个工具请求"
# 协议明文）检出。精确登记，防新差异静默溜入。
KNOWN_V32_GAP = {
    "runs/C": 1,        # 14-response.md：单 calls 块双 invoke（RUN+READ）
    "runs/T3/C15": 2,   # 03/04-response.md：双 calls 块各一 invoke
}


def _count_hits(run_dir: Path) -> int:
    hits = 0
    for f in sorted((run_dir / "turns").glob("*-response.md")):
        msg = f.read_text(errors="replace")
        rt = analyze(msg, "text")
        rd = analyze(msg, "dsml")
        total = max(rt.total_requests, rd.total_requests)
        if total > 1:
            hits += 1
    return hits


def test_multireq_regression_v32():
    failures = []
    for rel, expected in V32_TRUTH.items():
        d = MVP1_ROOT / rel
        if not d.exists():
            failures.append(f"{rel}: 目录缺失")
            continue
        got = _count_hits(d)
        expect = expected + KNOWN_V32_GAP.get(rel, 0)
        if got != expect:
            failures.append(f"{rel}: 期望 {expect}（V32 {expected}+已知差异）实测 {got}")
    assert not failures, "V32 回归差异：\n" + "\n".join(failures)
    # 检出语义本身：双请求 → detected、原因码结构齐全
    r = analyze("READ a\nWRITE b\nRUN c\nSend.", "text")
    assert r.detected and r.total_requests == 3
    assert r.executed_kind == "READ" and r.executed_index == 0   # 首请求执行
    assert r.dropped_kinds == ["WRITE", "RUN"]
    assert all(not t for t in r.dropped_full_texts) or r.dropped_full_texts  # 遥测留档
    r2 = analyze("READ only\nSend.", "text")
    assert not r2.detected and r2.total_requests == 1


# ── (e) audit-error 分类测试（含存疑从宽） ─────────────────────────

def test_audit_error_classification():
    # 数值化：阈值比较，无"适当超时"（120_000=不超时；120_001=超时）
    assert classify_oracle_timeout(119_999, "oracle") == ""
    assert classify_oracle_timeout(120_001, "oracle") == "ORACLETIMEOUT"
    assert classify_oracle_timeout(30_001, "per_test") == "ORACLETIMEOUT"
    assert classify_oracle_timeout(60_001, "run_tool") == "ORACLETIMEOUT"
    # 存疑从宽：无法判定 → 一律 audit-error（默认码）
    assert ambiguous_to_audit_error() == "ORACLEEXCEPTION"
    assert classify_selftest_fail() == "ORACLESELFTESTFAIL"
    assert classify_input_incomplete() == "ORACLEINPUTINCOMPLETE"
    ev = record_event("ORACLEEXCEPTION", "x", rerun_used=False)
    assert ev.detail_internal == "x"  # detail 入内部遥测、不出现在 agent 可见面
    assert ev.rerun_allowed is True                  # 首次：允许一次重跑
    with pytest.raises(ValueError):
        record_event("NOT-A-CODE", "x", rerun_used=False)   # 四类外拒绝


# ── (f) 覆盖表生成与不可见性 ─────────────────────────────────────

def test_coverage_artifact():
    # 无覆盖条款列示
    assert DRAFT_TABLE.uncovered_requirements() == ["EC-1"]
    # 覆盖率
    assert DRAFT_TABLE.coverage_rate() == 0.75
    # 研究工件渲染
    art = DRAFT_TABLE.render_research_artifact()
    assert "无覆盖" in art and "EC-1" in art
    # 不可见性：工件全文不在 agent 可见物中
    visible = ["任务规格文本", f"反馈：{FIXED_RECEIPT_TEXT}", "mechanics 概述"]
    assert DRAFT_TABLE.check_agent_invisible(art, visible) is True
    assert DRAFT_TABLE.check_agent_invisible(art, visible + [art]) is False


# ── 附加：双带判据纯函数（校准脚手架可编排性） ───────────────────

def test_dual_band():
    v = evaluate_dual_band(n_runs=10, n_done=6, n_first_done_failed=3)
    assert v.done_rate == 0.6 and abs(v.first_fail_rate - 0.5) < 1e-9
    assert v.in_band is True
    v2 = evaluate_dual_band(n_runs=10, n_done=2, n_first_done_failed=0)
    assert v2.in_band is False                       # done_rate 0.2 < 0.5 带外
    assert "无 DONE" not in v2.reason
    v3 = evaluate_dual_band(n_runs=10, n_done=0, n_first_done_failed=0)
    assert v3.in_band is False and "无 DONE" in v3.reason
    # 更换规则
    assert replacement_rule(True, 1, 3).startswith("REPLACE")
    assert replacement_rule(True, 3, 3).startswith("STOP")     # 禁无限重复
    assert replacement_rule(False, 1, 3).startswith("IN_BAND")
