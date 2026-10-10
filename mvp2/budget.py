r"""S8-1｜F/M/N 三计数器与状态机（v0.2-frozen S2）

状态生命周期（单运行）：
  WORKING --首次 DONE--> DONE_DECLARED --验收--> (PASS -> 终局)
     |                                   \--FAIL--> FEEDBACK(扣F)
     |--N 耗尽(T=0)--> [终态审计 if 开]
     |                                    M 可用 -> REPAIR(M 计数)
     |                                    M 耗尽 -> FAILED_UNVERIFIED
终止态：VERIFIED / FAILED_UNVERIFIED / AUDIT_ERROR / CAP

冻结口径（S2 + D-020 §4.4）：
- N=30 工作轮（首次完成阶段）；M=5 修复轮（仅可在收到失败反馈后
  使用；M 耗尽→不再启动修复，未过验收=failed-unverified）；
  F=5 反馈事件（每次携带协议信息的验收失败反馈扣 1）；
- 总轮硬上限 = N+M = 35（派生）；T=0 为唯一硬终止；
- audit-error 三不：不扣 N/M/F、不计 agent 失败、统计分母单列；
- 同 run 允许一次重跑（单独记录，禁止静默池化）；
- 四组总预算口径一致（A 臂 M/F 自然闲置，总轮次上限相同）。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .constants import ARMS, F_FEEDBACK, M_REPAIR, N_WORK, TOTAL_ROUNDS


class Phase(str, Enum):
    WORKING = "working"            # N 计数阶段（首次完成）
    DONE_DECLARED = "done_declared"  # 首次 DONE 声明后的验收分支（B/D 臂）
    FEEDBACK = "feedback"          # 携带协议信息的失败反馈已发（扣 F）
    REPAIR = "repair"              # M 计数阶段
    FINAL_AUDIT = "final_audit"    # 终态审计阶段（C/D 臂，N 耗尽后）
    # 终止态（互斥；值与 S6 交付三态一致）：
    VERIFIED = "verified"
    FAILED_UNVERIFIED = "failed-unverified"
    AUDIT_ERROR = "audit-error"
    CAP = "cap"                    # T=0 唯一硬终止（预算外）

    @property
    def is_terminal(self) -> bool:
        return self in (
            Phase.VERIFIED,
            Phase.FAILED_UNVERIFIED,
            Phase.AUDIT_ERROR,
            Phase.CAP,
        )


class BudgetError(RuntimeError):
    """预算模型违规（状态机使用方错误，非 agent 失败）。"""


@dataclass
class BudgetState:
    arm: str                        # A/B/C/D（S4）
    n_used: int = 0
    m_used: int = 0
    f_used: int = 0
    phase: Phase = Phase.WORKING
    repairs_started: bool = False   # M 是否已获授权（收到失败反馈）
    rerun_flag: bool = False        # audit-error 单次重跑是否已用（D-020 §4.4）
    event_log: list = field(default_factory=list)

    def _log(self, ev: str) -> None:
        self.event_log.append((self.n_used, self.m_used, self.f_used, ev))

    # ── 阶段推进（WORKING：每工作轮消耗 N）────────────────────
    def consume_work(self) -> bool:
        """消费一个工作轮。

        返回 True=本轮消费成功；False=本轮为 N 末轮（本轮已计入，
        T=0 触发：终态审计开→FINAL_AUDIT，关→CAP）。
        N 已耗尽后调用 → BudgetError（使用方错误）。
        """
        if self.phase is not Phase.WORKING:
            raise BudgetError(f"N 只能在 working 阶段消耗，当前 {self.phase}")
        if self.n_used >= N_WORK:
            raise BudgetError("N 已耗尽")
        self.n_used += 1
        self._log("work")
        if self.n_used == N_WORK:
            # N 耗尽 → 终态审计开（C/D）转 FINAL_AUDIT；关（A/B）转 CAP
            if ARMS[self.arm]["final_audit"]:
                self.phase = Phase.FINAL_AUDIT
            else:
                self.phase = Phase.CAP
            self._log("n_exhausted")
            return False
        return True

    # ── DONE 门（B/D 臂；A/C "关"= 不暴露不阻断不修复，仍离线测量）──
    def declare_done(self) -> None:
        gate_open = ARMS[self.arm]["done_gate"]
        if not gate_open:
            # A/C：声明不触发门（离线测量另行记录），预算面无变化
            self._log("done_declared_gate_closed")
            return
        if self.phase is not Phase.WORKING:
            raise BudgetError(f"DONE 声明只接受一次，当前 {self.phase}")
        # DONE 声明轮计入 N（首次完成阶段末轮；末轮 DONE 合法：
        # T3-A@30 先例——验收过=VERIFIED，不过=扣 F 进 M）
        self.n_used += 1
        if self.n_used > N_WORK:
            raise BudgetError("DONE 声明超出 N 预算（T=0 后不接受新 DONE）")
        self.phase = Phase.DONE_DECLARED
        self._log("done_declared")

    # ── 验收失败反馈（扣 F；仅携带协议信息的反馈才扣）────────────
    def accept_feedback(self) -> None:
        if self.f_used >= F_FEEDBACK:
            # F 已耗尽 → 调用方应发 FIXED_RECEIPT（不扣、不含协议信息）
            raise BudgetError("F 已耗尽——此时应注入固定回执而非协议反馈")
        self.f_used += 1
        self.repairs_started = True   # 收到失败反馈后 M 才可使用（S2）
        self.phase = Phase.FEEDBACK
        self._log("feedback")

    # ── 修复轮（M 计数）────────────────────────────────────────
    def consume_repair(self) -> None:
        if not self.repairs_started:
            raise BudgetError("M 仅可在收到失败反馈后使用（S2 冻结）")
        if self.m_used >= M_REPAIR:
            raise BudgetError("M 已耗尽——不得再启动修复")
        if self.n_used + self.m_used >= TOTAL_ROUNDS:
            self.phase = Phase.CAP
            self._log("total_cap")
            return
        self.m_used += 1
        self.phase = Phase.REPAIR
        self._log("repair")

    def m_exhausted_unverified(self) -> bool:
        """M 耗尽且未过验收 → failed-unverified（终局判定辅助）。"""
        return self.repairs_started and self.m_used >= M_REPAIR

    # ── audit-error 三不 + 单次重跑（D-020 §4.4）────────────────
    def register_audit_error(self, code: str) -> None:
        """不扣 N/M/F、不计 agent 失败、分母单列；允许一次重跑。"""
        from .constants import AUDIT_ERROR_CODES
        if code not in AUDIT_ERROR_CODES:
            raise BudgetError(f"未知原因码 {code}")
        if self.rerun_flag:
            # 第二次 audit-error：不再重跑，按终局 audit-error 记
            self.phase = Phase.AUDIT_ERROR
            self._log(f"audit_error_final:{code}")
            return
        self.rerun_flag = True
        self._log(f"audit_error_rerun:{code}")  # 预算面零变化（三不）

    # ── 终局 ──────────────────────────────────────────────────
    def finalize(self, outcome: str) -> None:
        assert outcome in ("verified", "failed-unverified")
        self.phase = Phase.VERIFIED if outcome == "verified" else Phase.FAILED_UNVERIFIED
        self._log(f"final:{outcome}")

    # 审计用快照
    def snapshot(self) -> dict:
        return {
            "arm": self.arm,
            "phase": self.phase.value,
            "n_used": self.n_used,
            "m_used": self.m_used,
            "f_used": self.f_used,
            "total_rounds": self.n_used + self.m_used,
            "repairs_started": self.repairs_started,
            "rerun_flag": self.rerun_flag,
        }
