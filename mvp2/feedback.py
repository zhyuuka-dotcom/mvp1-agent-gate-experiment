"""S8-3｜白名单填充模板（明示项路径，v0.2-frozen S3）

明示项（披露许可线上的要求）：反馈 = 冻结模板 + 白名单字段
结构化填充。执行器只有"填格权"、无"诊断生成权"——即值只能取自
神谕冻结工件预登记的枚举，任何模板外文本/自生成诊断在构造期即拒。

字段结构（预冻结；WP-1 起草，WP-2 前 PI 核）：
  - {FAILED_CATEGORIES}  全部失败类别 ID 列表（单次披露范围=全部
    失败类别，S3 冻结——刻意设计，测类别提示引导推断未明示要求的
    能力）
  - {REMAINING_M}        M 剩余额度（数字，来自 BudgetState）
  - {REMAINING_F}        F 剩余额度（数字）
动态失败计数（每类别出现次数）**移出 agent 可见反馈**，入内部遥测。
"""
from __future__ import annotations

import string
from dataclasses import dataclass

from .budget import BudgetState

TEMPLATE = (
    "验收未通过。失败的验收类别：$FAILED_CATEGORIES。"
    "剩余修复轮 $REMAINING_M，剩余反馈额度 $REMAINING_F。"
)

# 白名单：可填充字段的唯一合法值域（枚举式；运行时零生成）
ALLOWED_FIELDS = {
    "FAILED_CATEGORIES": lambda ctx: " ".join(
        sorted(ctx["failed_categories"])  # 值=预冻结 EC 句柄（hidden_corpus）
    ),
    "REMAINING_M": lambda ctx: str(ctx["remaining_m"]),
    "REMAINING_F": lambda ctx: str(ctx["remaining_f"]),
}

_SAFE = string.Template(TEMPLATE)


class FeedbackValueError(ValueError):
    """白名单外取值/模板外字段 → 构造期拒绝（执行器无诊断生成权）。"""


def render_feedback(
    budget: BudgetState,
    failed_categories: set[str],
    corpus=None,
) -> str:
    """明示项反馈：模板 + 白名单填充。

    failed_categories：只能取自神谕冻结的类别句柄（冻结校验：
    形态 EC-k ∧ 存在于冻结语料表——运行时不得引入新句柄，S3）。
    corpus：冻结语料（默认 hidden_corpus.DRAFT_CORPUS；正式运行
    时为任务包冻结件）。
    """
    if corpus is None:
        from .hidden_corpus import DRAFT_CORPUS as corpus
    ctx = {
        "failed_categories": sorted(failed_categories),
        "remaining_m": 5 - budget.m_used,
        "remaining_f": 5 - budget.f_used,
    }
    # 结构校验：句柄形态 EC-k ∧ 冻结在案（执行器无诊断生成权）
    for c in ctx["failed_categories"]:
        if not _is_ec_handle(c):
            raise FeedbackValueError(f"非白名单类别句柄：{c!r}（执行器无诊断生成权）")
        if c not in corpus.mapping:
            raise FeedbackValueError(f"未冻结句柄 {c!r}——运行时不得引入新句柄（S3）")
    return _SAFE.substitute(
        FAILED_CATEGORIES=ALLOWED_FIELDS["FAILED_CATEGORIES"](ctx),
        REMAINING_M=ALLOWED_FIELDS["REMAINING_M"](ctx),
        REMAINING_F=ALLOWED_FIELDS["REMAINING_F"](ctx),
    )


def _is_ec_handle(c: str) -> bool:
    import re
    return bool(re.fullmatch(r"EC-[0-9]+", c))
