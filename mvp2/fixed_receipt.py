"""S8-2｜固定回执注入（v0.2-frozen S2 F 条款 + S3）

F 耗尽后，验收失败反馈一律替换为预冻结固定文本：
  ① 逐字节等于 constants.FIXED_RECEIPT_TEXT；
  ② 零动态信息：不含失败计数/类别/观测值/路径/堆栈；
  ③ 内容不随隐藏失败情况变化（自测 b：任意隐藏失败组合逐字节相同）。
"""
from __future__ import annotations

from .constants import FIXED_RECEIPT_TEXT
from .budget import BudgetState


def fixed_receipt(budget: BudgetState) -> str:
    """F 耗尽后的验收失败回执。唯一实现路径，禁止任何插值。"""
    if budget.f_used < 5:
        raise RuntimeError("F 未耗尽——不应注入固定回执（协议反馈路径仍可用）")
    return FIXED_RECEIPT_TEXT


class _Sanitizer:
    """设计级守卫：供静态审查/自测证明固定回执无动态成分。

    不参与运行时注入（运行时只调用 fixed_receipt()）。
    """

    FORBIDDEN_SUBSTRINGS = (
        "failed", "FAIL", "count", "次", "类别", "category",
        "path", "路径", "traceback", "堆栈", "观测",
    )

    @classmethod
    def check_invariance(cls) -> bool:
        return all(s not in FIXED_RECEIPT_TEXT for s in cls.FORBIDDEN_SUBSTRINGS)
