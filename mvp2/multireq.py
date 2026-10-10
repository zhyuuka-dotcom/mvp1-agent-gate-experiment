"""S8-5｜MULTI_REQ 检测与原因码（D-021 §5 阶段 1；口径源 D-019 §2.4）

执行策略（MVP-2 冻结，v0.2 §2.4 同源）：
  单步执行保持——每消息仅执行首个工具请求；
  回执强制 MULTI_REQ 原因码：列明全部请求及各自处置（执行/丢弃），
  丢弃请求全文入遥测。
不改"执行全部"——透明化优先于扩权，保留模型协议习惯作为被测行为。

检测方法复用 V32 扫描器（runs/V32-multi-request-scan.md 方法学）：
  文本协议计 ^WRITE/^READ/^RUN 行首模式；
  DSML 协议计 invoke 块数。
首请求选择规则（与 MVP-1 驱动器一致，保持被测行为可比）：
  首个出现的工具请求执行，其余丢弃（V32 报告的执行选择规则为
  READ 取末/RUN 取末——MVP-1 现役行为；MVP-2 冻结为"首个"以使
  原因码语义恒定。**差异点登记**：V32 语料回归按"命中检出"校验
  （与选择规则无关），选择规则变化不影响回归测试集有效性。）
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# V32 方法学正则（文本协议）
TEXT_TOOL_RE = re.compile(r"^(WRITE|READ|RUN)\b", re.MULTILINE)
# DSML invoke 块（MVP-1 后期协议）
DSML_INVOKE_RE = re.compile(r"<｜｜DSML｜｜ invoke name=\"(WRITE|READ|RUN)\">")
# 文件末行退出哨兵（MVP-1 文本协议的 Send. 终止行不计为工具请求）
SEND_LINE_RE = re.compile(r"^Send\.", re.MULTILINE)


@dataclass
class MultiReqReport:
    detected: bool
    total_requests: int
    executed_index: int            # 恒 0（首请求执行，MVP-2 冻结）
    executed_kind: str
    dropped_kinds: list[str] = field(default_factory=list)
    dropped_full_texts: list[str] = field(default_factory=list)  # 入遥测（S7）

    def receipt_reason_code(self) -> str:
        """回执原因码（S7 机器可读）。

        单请求消息 → 空串（不携带 MULTI_REQ 码）；
        多请求消息 → "MULTI_REQ"（回执正文另列全部请求及处置）。
        """
        return "MULTI_REQ" if self.detected else ""

    def receipt_lines(self) -> list[str]:
        """回执正文行：列明全部请求及各自处置（执行/丢弃）。"""
        lines = []
        for i, (kind, executed) in enumerate(self.request_flags):
            lines.append(f"[{i}] {kind}: {'EXECUTED' if executed else 'DROPPED'}")
        return lines

    # request_flags 由 analyze() 填充（dataclass 简化：构造后设置）
    request_flags: list = field(default_factory=list)


def _split_text_requests(message: str) -> list[tuple[str, str]]:
    """文本协议：每个 ^WRITE/^READ/^RUN 行 = 一个请求（行文本为全文）。"""
    out = []
    for m in TEXT_TOOL_RE.finditer(message):
        start = m.start()
        line_end = message.find("\n", start)
        line = message[start:line_end if line_end != -1 else len(message)]
        out.append((m.group(1), line))
    return out


def _split_dsml_requests(message: str) -> list[tuple[str, str]]:
    """DSML 协议：每个 invoke 块 = 一个请求（块全文为丢弃留档文本）。"""
    out = []
    for m in DSML_INVOKE_RE.finditer(message):
        start = m.start()
        # 块终点 = 下一个 invoke 起点或消息尾
        nxt = DSML_INVOKE_RE.search(message, m.end())
        block = message[start:nxt.start() if nxt else len(message)]
        out.append((m.group(1), block))
    return out


def analyze(message: str, protocol: str = "text") -> MultiReqReport:
    """检测一条 agent 消息中的工具请求数与首请求。

    protocol: "text"（T2/T3 风格行首协议）或 "dsml"（invoke 块协议）。
    首请求选择 = 索引 0（MVP-2 冻结）。
    """
    reqs = _split_text_requests(message) if protocol == "text" else _split_dsml_requests(message)
    kinds = [k for k, _ in reqs]
    report = MultiReqReport(
        detected=len(reqs) > 1,
        total_requests=len(reqs),
        executed_index=0 if reqs else -1,
        executed_kind=kinds[0] if kinds else "",
        dropped_kinds=kinds[1:],
        dropped_full_texts=[t for _, t in reqs[1:]],
        request_flags=[(k, i == 0) for i, k in enumerate(kinds)],
    )
    return report
