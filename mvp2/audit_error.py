"""S8-6｜audit-error 分支（D-020 §4 四条冻结细则）

  ① 存疑从宽：分类不确定（无法判定验收器异常 vs agent 产物问题）
     一律 audit-error——基础设施失败误计入 agent 失败是本项目两次
     付出代价的归因错误（C 臂截断墙、E30 假失败），制度上禁止第三次；
  ② 超时数值化：具体毫秒值见 constants（建议值待 PI 核后冻结）；
  ③ 原因码强制：ORACLEEXCEPTION / ORACLETIMEOUT /
     ORACLESELFTESTFAIL / ORACLEINPUTINCOMPLETE 四类起步；
  ④ 统计处置：不扣 N/M/F、不计 agent 失败、分母单列；
     同 run 允许一次重跑（单独记录，禁止静默池化）。
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .constants import (
    AUDIT_ERROR_CODES,
    ORACLE_PER_TEST_TIMEOUT_MS,
    ORACLE_TIMEOUT_MS,
    RUN_TOOL_TIMEOUT_MS,
)


class AuditErrorKind(str, Enum):
    ORACLEEXCEPTION = "ORACLEEXCEPTION"            # 验收器抛异常
    ORACLETIMEOUT = "ORACLETIMEOUT"                # 验收器超时（数值化阈值）
    ORACLESELFTESTFAIL = "ORACLESELFTESTFAIL"      # 验收器自测失败（S7 自身验证记录）
    ORACLEINPUTINCOMPLETE = "ORACLEINPUTINCOMPLETE"  # 验收输入不完整（快照/语料缺失）


@dataclass
class AuditErrorEvent:
    code: str
    detail_internal: str            # 入内部遥测（agent 不可见）
    elapsed_ms: int | None = None
    rerun_allowed: bool = True      # 首次 True；同 run 第二次 False（禁静默池化）


def classify_oracle_exc() -> str:
    return AuditErrorKind.ORACLEEXCEPTION.value


def classify_oracle_timeout(elapsed_ms: int, which: str = "oracle") -> str:
    """超时分类（②数值化：阈值常量比较，无"适当超时"措辞）。

    which: "oracle"（整体）/ "per_test"（单测试）/ "run_tool"（RUN 工具）
    """
    thresholds = {
        "oracle": ORACLE_TIMEOUT_MS,
        "per_test": ORACLE_PER_TEST_TIMEOUT_MS,
        "run_tool": RUN_TOOL_TIMEOUT_MS,
    }
    if elapsed_ms <= thresholds[which]:
        return ""  # 未超时：非 audit-error（正常路径）
    return AuditErrorKind.ORACLETIMEOUT.value


def classify_selftest_fail() -> str:
    return AuditErrorKind.ORACLESELFTESTFAIL.value


def classify_input_incomplete() -> str:
    return AuditErrorKind.ORACLEINPUTINCOMPLETE.value


def ambiguous_to_audit_error() -> str:
    """①存疑从宽：任何无法判定验收器异常 vs agent 产物问题的情形。"""
    return AuditErrorKind.ORACLEEXCEPTION.value  # 从宽默认码


def record_event(code: str, detail: str, *, rerun_used: bool) -> AuditErrorEvent:
    if code not in AUDIT_ERROR_CODES:
        raise ValueError(f"未知原因码 {code}（四类起步，实施包增补须 PI 核）")
    return AuditErrorEvent(
        code=code,
        detail_internal=detail,
        rerun_allowed=not rerun_used,  # 同 run 仅一次重跑（④）
    )
