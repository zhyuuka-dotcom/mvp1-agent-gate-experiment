"""S8-9｜双带校准脚手架（v0.2-frozen S5；可编排、不可运行）

  校准结构（冻结）：
  - 裸 A 基线；固定模型配置与预算；校准样本 n=10 冻结；
  - 双带联合判据：DONE 产出率 ∈ [50%, 80%]（分母=全部有效校准运行）
    ∧ 首验失败率 ∈ [30%, 70%]（分母=出现首次 DONE 的运行；
    无 DONE 的运行不计入"低于 30%"）；
  - 更换规则：带外 → 按预冻结候选清单更替任务 → 新校准轮（n=10
    重跑）；禁止无限重复至偶然合意；
  - 全部校准运行与更换记录留档、不得用于正式效果估计；
    校准与正式样本严格分离，正式样本冻结点 = 双带命中后的 commit。

  本模块只提供"编排描述"与"判据计算"（纯函数）——不调用任何
  agent API、不启动任何运行（WP-2 校准运行授权前纪律）。
"""
from __future__ import annotations

from dataclasses import dataclass

from .constants import CALIBRATION_N, DONE_RATE_BAND, FIRST_FAIL_BAND


@dataclass
class CalibrationRoundPlan:
    """一轮校准的编排计划（描述性；执行需 WP-2 授权）。"""
    round_no: int
    task_id: str
    n: int = CALIBRATION_N
    arm: str = "A"        # 裸 A 基线（冻结）
    authorized: bool = False  # WP-2 前 False


@dataclass
class DualBandVerdict:
    done_rate: float          # 分母 = 全部有效校准运行
    first_fail_rate: float    # 分母 = 出现首次 DONE 的运行（无 DONE 不计）
    n_runs: int
    n_runs_with_done: int
    in_band: bool
    reason: str

    def __str__(self) -> str:  # 审计留档用
        return (
            f"calibration round verdict: done_rate={self.done_rate:.2f} "
            f"first_fail={self.first_fail_rate:.2f} in_band={self.in_band} ({self.reason})"
        )


def evaluate_dual_band(
    n_runs: int, n_done: int, n_first_done_failed: int
) -> DualBandVerdict:
    """双带联合判据（纯函数）。

    n_runs：全部有效校准运行数；
    n_done：产出 DONE 的运行数；
    n_first_done_failed：出现首次 DONE 且首验失败的运行数
    （分母 = 出现首次 DONE 的运行；无 DONE 的运行不计入
    "低于 30%"——即首验失败率分母 = n_done，本实现口径注记：
    "出现首次 DONE"与"产出 DONE"在有 DONE 即首次的 MVP-2 单
    DONE 设计下同集合；若未来允许多次 DONE 声明，分母须改用
    出现首次 DONE 的运行数——登记为设计注记）。
    """
    if n_runs <= 0:
        raise ValueError("n_runs 必须为正（校准样本 n=10 冻结）")
    done_rate = n_done / n_runs
    first_fail_rate = (n_first_done_failed / n_done) if n_done > 0 else float("nan")
    lo, hi = DONE_RATE_BAND
    flo, fhi = FIRST_FAIL_BAND
    ok_done = lo <= done_rate <= hi
    ok_fail = n_done == 0 or (flo <= first_fail_rate <= fhi)
    in_band = ok_done and ok_fail
    reason = (
        f"done_rate {done_rate:.2f} {'∈' if ok_done else '∉'} [{lo},{hi}]"
        + (f"; first_fail {first_fail_rate:.2f} {'∈' if ok_fail else '∉'} [{flo},{fhi}]" if n_done > 0
           else "; 无 DONE 运行：首验失败率带不计入")
    )
    return DualBandVerdict(
        done_rate=done_rate,
        first_fail_rate=first_fail_rate,
        n_runs=n_runs,
        n_runs_with_done=n_done,
        in_band=in_band,
        reason=reason,
    )


def replacement_rule(out_of_band: bool, round_no: int, max_rounds: int) -> str:
    """更换规则：带外 → 预冻结候选清单更替任务 → 新校准轮。

    禁止无限重复至偶然合意（max_rounds 上限后必须停下上报 PI）。
    """
    if not out_of_band:
        return "IN_BAND: 冻结正式样本冻结点（双带命中后的 commit）"
    if round_no >= max_rounds:
        return "STOP: 校准轮上限已达——禁止无限重复至偶然合意，上报 PI 裁"
    return f"REPLACE: 按预冻结候选清单更替任务 → 第 {round_no + 1} 轮（n=10 重跑）"
