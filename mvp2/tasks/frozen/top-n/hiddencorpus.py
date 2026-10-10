"""hiddencorpus 正式件｜任务 top-n（冻结 2026-10-11）"""
from __future__ import annotations

from mvp2.hidden_corpus import HiddenCorpus

TOP_N_CORPUS = HiddenCorpus(
    mapping={
        "EC-1": "N ≥ 总行数（全量）",
        "EC-2": "超大值健壮性",
        "EC-3": "非整数参数层拦截",
        "EC-4": "负数参数层拦截",
        "EC-5": "--top × -n 组合优先级",
    },
    strings={
        "EC-1": "边界：参数取值超出数据规模时行为与预期不符。请检查极端取值路径。",
        "EC-2": "边界：参数取值超出数据规模时行为与预期不符。请检查极端取值路径。",
        "EC-3": "错误处理：非法参数值未被参数层拦截。请检查参数校验的位置。",
        "EC-4": "错误处理：非法参数值未被参数层拦截。请检查参数校验的位置。",
        "EC-5": "兼容：功能与既有参数组合使用时行为异常。请检查参数交互的优先级。",
    },
)

RE_STRINGS = {
    "RE-1": "规格条款 1（--top 限流 Detailed 前 N 行）未满足：$RC，$OBS_STDOUT",
    "RE-2": "规格条款 5（零回归）未满足：$CHANGED_FILES",
    "RE-3": "规格条款 2（--top 0 仅表头）未满足：$RC，$OBS_STDOUT",
}
