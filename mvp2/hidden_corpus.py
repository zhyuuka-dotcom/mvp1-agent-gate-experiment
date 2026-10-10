"""S8-4｜隐藏语料注入（隐藏项路径，v0.2-frozen S3）

隐藏项（披露许可线下、agent 可见文本未明示的要求）：
  - 零运行时生成——反馈串/句柄全部预写，随神谕冻结；
  - 运行时仅"选择"，禁止任何插值填空；
  - 句柄 EC-k 不透明：ID→类别对照表冻结入档（研究工件），
    ID→要求映射**不存在于 agent 可见物**；
  - 运行时选择规则（顺序、去重、组合）预冻结：
      顺序 = 句柄 ID 升序；去重 = 同一反馈事件内同类别只出现一次；
      组合 = 与明示项反馈在同一模板的 FAILED_CATEGORIES 槽位合并。
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HiddenCorpus:
    """神谕冻结工件（起草件——正式 EC 表随任务包冻结，WP-2 前 PI 核）。

    mapping: EC-k 句柄 → 内部类别描述（对 agent 不可见；
             该表冻结入研究工件 coverage/）
    strings: 每句柄的预写反馈串（本版未用自由文本，句柄本身即披露；
             保留槽位以支撑未来无句柄形态，仍禁插值）
    """

    mapping: dict[str, str]
    strings: dict[str, str]

    def validate(self) -> None:
        assert set(self.mapping) == set(self.strings), "句柄表与反馈串表键集不一致"
        for k in self.mapping:
            assert _is_ec(k), f"非法句柄形态 {k}"

    def select(self, failed: set[str]) -> list[str]:
        """运行时选择：顺序=ID 升序，去重=set 语义，零生成零插值。"""
        for k in failed:
            if k not in self.mapping:
                raise KeyError(f"未冻结句柄 {k}——运行时不得引入新句柄")
        return sorted(failed, key=lambda k: int(k.split("-")[1]))


def _is_ec(k: str) -> bool:
    import re
    return bool(re.fullmatch(r"EC-[0-9]+", k))


# 起草样例（正式值随挑战集任务包冻结；此处供自测 c 泄漏测试用）
DRAFT_CORPUS = HiddenCorpus(
    mapping={
        "EC-1": "错误处理缺失（隐藏要求示例）",
        "EC-2": "边界条件未覆盖（隐藏要求示例）",
        "EC-3": "兼容回退缺失（隐藏要求示例）",
    },
    strings={"EC-1": "", "EC-2": "", "EC-3": ""},
)
