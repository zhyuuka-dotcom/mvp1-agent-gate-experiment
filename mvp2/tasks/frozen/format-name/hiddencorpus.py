"""hiddencorpus 正式件｜任务 format-name（冻结 2026-10-11）"""
from __future__ import annotations

from mvp2.hidden_corpus import HiddenCorpus

FORMAT_NAME_CORPUS = HiddenCorpus(
    mapping={
        "EC-1": "同名 log_format 指令歧义（取首个）",
        "EC-2": "带引号格式名匹配",
        "EC-3": "名解析与 --no-follow 兼容",
        "EC-4": "名字大小写敏感",
    },
    strings={
        "EC-1": "分组：同名配置指令的取值歧义未被正确处理。请检查配置解析的选取规则。",
        "EC-2": "兼容：配置文件语法的引号形态未被支持。请检查名字解析的语法覆盖。",
        "EC-3": "兼容：功能与既有参数组合使用时行为异常。请检查参数交互。",
        "EC-4": "边界：名字匹配规则与预期不符。请检查匹配的精确性。",
    },
)

RE_STRINGS = {
    "RE-1": "规格条款 1（-f 名字引用解析）未满足：$RC，$OBS_STDOUT",
    "RE-2": "规格条款 2（格式串零回归）未满足：$CHANGED_FILES",
    "RE-3": "规格条款 3（未知名报错）未满足：$RC，$OBS_STDOUT",
}
