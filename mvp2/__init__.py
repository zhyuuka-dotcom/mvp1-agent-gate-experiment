"""mvp2 — MVP-2 实施包（WP-1 产出，授权链 D-021 §3/§5）

九项 ↔ 模块地图（S8 → 文件）：
  1 F/M/N 计数器与状态机       budget.py
  2 固定回执注入               fixed_receipt.py
  3 白名单填充模板             feedback.py
  4 隐藏语料注入               hidden_corpus.py
  5 MULTI_REQ 检测+原因码      multireq.py
  6 audit-error 分支           audit_error.py
  7 覆盖表工件                 coverage.py
  8 指标遥测字段（S6 规格）    telemetry_spec.md
  9 双带校准脚手架             calibration.py

纪律：本包不触碰任何 MVP-1 冻结件；不改动现役 MVP-1 驱动器；
不开任何 agent 运行（含校准——WP-2 授权前）。
"""
