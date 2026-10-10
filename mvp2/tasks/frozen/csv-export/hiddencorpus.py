"""hiddencorpus 正式件｜任务 csv-export（冻结 2026-10-10，D-022 §3(b)）

替换 mvp2/hidden_corpus.DRAFT_CORPUS 引用（正式运行时）。
S3 纪律：句柄 EC-k 不透明（ID→类别对照表冻结入研究工件
COVERAGE.md，ID→要求映射不存在于 agent 可见物）；
零运行时生成——本表预写随神谕冻结。
"""
from __future__ import annotations

from mvp2.hidden_corpus import HiddenCorpus

CSV_EXPORT_CORPUS = HiddenCorpus(
    mapping={
        # 句柄 → 内部类别描述（对 agent 不可见；与 COVERAGE.md 一致）
        "EC-1": "空数据边界（count=0 行如实输出）",
        "EC-2": "--csv 与 --no-follow 参数兼容",
        "EC-3": "含逗号字段 RFC 4180 引号转义",
    },
    strings={
        # 隐藏项反馈串（三重预写：句柄+标签+通用提示；零插值）
        "EC-1": "边界：某个输入条件下的行为与预期不符。请检查特殊输入情形。",
        "EC-2": "兼容：功能与既有参数组合使用时行为异常。请检查参数交互。",
        "EC-3": "错误处理：输出内容的正确性规则未满足。请检查输出内容的格式正确性规则。",
    },
)

RE_STRINGS = {
    # 明示项反馈串（规格条款引文模板，白名单字段占位 $RC 等
    # 由执行器填格——填充值域冻结于 FEEDBACK.md）
    "RE-1": "规格条款 1（--csv 布尔开关）未满足：$RC，$OBS_STDOUT",
    "RE-2": "规格条款 2 前半（列头=表列序，逗号分隔）未满足：$OBS_STDOUT",
    "RE-3": "规格条款 2 后半（数值与人类可读模式一致）未满足：$OBS_STDOUT",
    "RE-4": "规格条款 3（无 --csv 零回归）未满足：$CHANGED_FILES",
}
