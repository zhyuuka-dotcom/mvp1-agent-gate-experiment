"""S8-7｜覆盖表工件（v0.2-frozen S6/S7）

  - 每个验收测试 ↔ 要求条款（EC-k 明示 / RE-k 隐藏）的映射表；
  - 无覆盖条款列示：哪些要求没有任何测试覆盖（verified ≠ 满足
    全部规格——覆盖缺口注记随结果披露）；
  - 冻结为研究工件、**不对 agent 可见**（S7）。
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoverageTable:
    requirement_to_tests: dict[str, tuple[str, ...]]  # 要求句柄 → 验收测试 ID 元组
    all_tests: tuple[str, ...]                        # 验收套件全部测试 ID

    def uncovered_requirements(self) -> list[str]:
        """无覆盖条款（验收套件测不到的要求）。"""
        return sorted(k for k, v in self.requirement_to_tests.items() if not v)

    def coverage_rate(self) -> float:
        covered = sum(1 for v in self.requirement_to_tests.values() if v)
        return covered / len(self.requirement_to_tests)

    def render_research_artifact(self) -> str:
        """研究工件渲染（冻结存档；进入 repo-snapshot/归档，不进 agent 可见面）。"""
        lines = ["# 覆盖表（研究工件，不对 agent 可见）", ""]
        for k in sorted(self.requirement_to_tests):
            tests = ", ".join(self.requirement_to_tests[k]) or "（无覆盖）"
            lines.append(f"- {k}: {tests}")
        lines.append("")
        lines.append(f"覆盖缺口（无覆盖条款）：{', '.join(self.uncovered_requirements()) or '无'}")
        return "\n".join(lines)

    @staticmethod
    def check_agent_invisible(artifact_text: str, agent_visible_texts: list[str]) -> bool:
        """不可见性验证（自测 f）：工件全文不出现在任何 agent 可见文本中。"""
        return all(artifact_text not in t for t in agent_visible_texts)


# 起草样例（正式覆盖表随挑战集任务包冻结）
DRAFT_TABLE = CoverageTable(
    requirement_to_tests={
        "RE-1": ("T_spec_1", "T_spec_2"),
        "RE-2": ("T_edge_1",),
        "EC-1": (),
        "EC-2": ("T_hidden_1",),
    },
    all_tests=("T_spec_1", "T_spec_2", "T_edge_1", "T_hidden_1"),
)
