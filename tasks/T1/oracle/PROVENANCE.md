# T1 Hidden Oracle — Provenance 分类（审计要求，2026-10-07）

> 规则（审计原文）：issue-direct = issue 明确要求；behavior-derived = 冻结公开行为/fixture 合理推出；
> convention-derived = 仓库已有公开行为惯例。无法归三类 → ORACLE_REVIEW_REQUIRED。
> **本文件为冻结后附加文档：oracle 测试文件零改动、语义零改动、8/8 通过标准零改动。**
> 分类只做来源标注，不因实验结果偏好调整（无一条按"更容易成功/失败"移动类别）。

## 逐条分类

| # | 测试 | 分类 | 依据 |
|---|------|------|------|
| 1 | test_named_format_single_line | **issue-direct**（混合注记） | issue #108 原文给出命令形态（`-f main -l <file> --no-follow`）与症状（无结果行）；断言"处理出记录 + rc 0"= 症状的直接否定。混合注记：`5 records` 具体值与 Summary 数值（1626.6/状态分布）来自 fixture 手算与公开输出格式——次级依据 behavior-derived；"应处理出记录并给统计"本身是 issue 直述 |
| 2 | test_named_format_multiline | **issue-direct** | issue 原文的 log_format 定义即多行三段引号形式；nginx_multiline.conf 逐字复刻原文。与 #1 同构，仅 conf 换为原文形态 |
| 3 | test_stats_match_log_content | **behavior-derived** ⚠审计点名 | issue 只要求"出现结果行"，未要求数值正确。断言（Detailed 表 request_path="/" 计 2）的正确性标准来自 (a) fixture 确定内容手算 (b) ngxtop 冻结公开行为契约：工作格式（直传格式串）下输出即这些值——"修好"合理等价于"输出与工作格式时一致"。承认：本条比 issue 原文强，标 behavior-derived 而非伪装 issue-direct |
| 4 | test_named_format_selects_right_one | **issue-direct**（构造说明） | issue 核心语义 = "-f main 指代用户定义的、名为 main 的 log_format"（原文：定义 main + 引用 main）。名字→特定格式映射即 issue 语义。构造说明：双格式 conf（main+extra）为测试探针，非 issue 场景，但判据（解析到 main 而非 extra）纯出 issue 语义，无后验偏好 |
| 5 | test_unknown_name_clean_error | **convention-derived** ⚠审计点名 | issue 未涉及未知名行为。断言标准（rc≠0 + 指向格式的错误信息 + 无 traceback）来自仓库既有惯例：detect_log_config 对配置内错误格式名走 error_exit("Incorrect format name set in config…")——同型输入在既有路径得干净错误，本条要求修复路径与惯例一致。**承认这是实验者对"合理修复形态"的期望（惯例对齐），非 issue 要求；冻结时的 provenance 注释已如实标注"惯例派生"** |
| 6 | test_direct_format_string_unchanged | **behavior-derived** | 冻结公开行为：`-f` 直传完整格式串工作（冻结前实测 5 条；docopt usage `-f <format>` 语义）。回归保持 |
| 7 | test_default_combined_unchanged | **behavior-derived** | 冻结公开行为：默认 combined 解析（README 基本用法；特征化测试同源）。回归保持 |
| 8 | test_multi_group_by_unchanged | **behavior-derived** | 冻结公开行为：`-g a,b` 多列分组已支持（issue #27 已实现，冻结日实测双列输出）。回归保持 |

## 汇总与冲击面

- **issue-direct 4**（#1 #2 #4 + #1 的混合注记）；**behavior-derived 4**（#3 #6 #7 #8）；**convention-derived 1**（#5）；**ORACLE_REVIEW_REQUIRED 0**。
- 与冻结时"spec-direct 5 / edge 3"分组的关系（记录性映射，不改冻结分组）：
  原 spec-direct 5 = issue-direct 4 + convention-derived 1（#5）；原 edge 3 = behavior-derived 3；
  #3 原挂 spec-direct 组、现细标 behavior-derived。
- 对 A 臂的影响：无。A 的 FDV 判据 = 离线跑全部 8 条（8/8 通过才算 first_done_valid），回执分组计数只出现在 E 臂 FAIL 回执（E 未运行）。分类不改变任何断言、不改变 8/8 标准。
- 防作弊注记（非本次审计要求，顺带记录）：oracle 断言的具体数值（1626.6/状态分布/分组计数）由 fixture 内容锁死——agent 若篡改 repro/ 造假通过，git 快照 diff 会显形且数值断言难以伪造；fixtures 死变量 FIX_SRC（hidden 文件 line 22）未参与任何断言，留档不动。

## 审计点名的两条——结论

- test_unknown_name_clean_error：**convention-derived**，实验者后验偏好（错误风格）未伪装成 issue 要求（冻结时注释已声明"惯例派生，非 issue 直述"）。
- test_stats_match_log_content：**behavior-derived**，数值正确性由 fixture+公开行为契约推出，非 issue 原文要求——比原文强，但推导链可辩护且已如实标注。

两条均有诚实归类 → **无 ORACLE_REVIEW_REQUIRED → A 臂放行**。
