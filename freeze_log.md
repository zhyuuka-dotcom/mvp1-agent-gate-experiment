# MVP-1 冻结日志

## 时间线与审计顺序

- 2026-10-06：仓库遴选（ngxtop）→ T1/T2/T3 草案 → 评审裁决（T2 退回重找、
  T1 盲化规则、T3 保留）→ T2 issue 池穷尽（13 个 issue 全查，无合格项）→
  T2 转 Benchmark-authored 待最终裁决 → **T1 冻结（本提交）**
- 写入顺序（git 提交历史可验）：task.md → 特征化测试 → 隐藏神谕 +
  expected_stats.md → **root_cause_SEALED.md**（最后）
- 冻结前验证：
  - repo_frozen 基线：28 passed（存量 25 + 特征化 3）✅ F5 前半
  - 隐藏神谕红绿逻辑：spec-direct 5 红 / edge 3 绿 ✅ F5 后半
  - 神谕修正记录：原 edge#3（配置探测路径）在非 tty 子进程下不可达
    （`access_log is None and not isatty → 'stdin'`），已替换为
    `-g a,b` 多列分组保持测试（冻结日实测过的公开行为）。
    该发现同时进入 harness 协议注记：agent 的 RUN 亦为子进程，
    配置探测路径对 agent 同样不可达，不构成任务面。

## 仓库哈希

- repo_frozen（agent 工作副本源）：`a0891da4568dd2eb4ca1bd056fe56845bc5af8eb`
- 本目录（含神谕）整树提交哈希：见 mvp1 根 commit（提交后回填 README）

## relevant-files 推导（侦察覆盖率分母，防根因反推）

推导规则（机械，先于清单）：任务文本引用的 README/docopt 公开选项面
（`-f`、`-l`、`-c`、`--no-follow`、log_format 概念）+ 承载这些面的实现文件
+ 覆盖这些面的既有测试。

清单（4 项）：
1. `ngxtop/ngxtop.py`（CLI 入口与选项分派，docopt usage 所在）
2. `ngxtop/config_parser.py`（log_format 概念的解析面）
3. `tests/test_config_parser.py`（配置解析的既有测试参考）
4. `README.rst`（公开行为文档）

自检：根因封存件所指病灶仅 ngxtop.py；本清单**宽于**根因所需
（config_parser.py 与其测试按规格面规则保留在内），不存在收窄偏置。

## T2 猎寻记录（评审裁决执行）

- 开放 issue：#109（无输出规格）❌ #106（时间基准须实验者钉死）❌
  #100（薄规格）❌ #95（HAProxy 外部语义）❌ #107（内部改名，无行为增量，
  已划为非 bug 任务）❌ #108（→T1）✅ #105/#103（非代码任务）❌
- 关闭 issue 追查：#27 多列分组——**已在现行代码实现**（实测 `-g a,b` 正常）❌
  #104 HAProxy（变量映射语义=外部知识，F6 违规）❌ #74/#81（使用咨询）❌
  其余为环境/版本管理问题 ❌
- 结论：13/13 无合格 feature issue。按评审预设回退：
  **T2 = Benchmark-authored task（显式标注）**，语义由实验者撰写于任务文本，
  回答"完整规格下的执行纪律与自测覆盖"（另一问题，非侦察问题）。
  待评审方最终确认后冻结。

## 环境注记（harness 协议用）

- 依赖集冻结：docopt + tabulate + pyparsing + pytest（repo_frozen/.venv 预装，
  .gitignore 排除，freeze 时可由清单重建）
- docopt 库在 stderr 产生 SyntaxWarning：断言只看 stdout，warning 记噪声
- bash 会话当日多次 504 抖动：harness 的 RUN 走 repo venv 直调
  （`.venv/bin/python`），不走 uv run 动态解析——降抖动、离线、可复现
- 测试调用协议（两套必须分开调用，rootdir 不同）：
  1. repo 套件（28 条）：`cd repo_frozen && .venv/bin/python -m pytest tests/ -q`
  2. 隐藏神谕：`MVP1_REPO=<工作副本绝对路径> <任意 venv>/python -m pytest
     <mvp1>/tasks/T1/oracle/hidden/ -q`（对工作副本路径参数化，
     同一文件既服务 E 臂当场验收也服务 A/C 快照离线补测）
- 非/tty 注记：`process()` 在非 tty stdin 下将 access_log 置为 'stdin'，
  配置探测路径（detect_log_config）对子进程不可达——agent 的 RUN 与
  harness 同构，故该路径不构成任务面；原 edge#3 因此替换

## 冻结根哈希（mvp1 外层仓库）

- `34f1d8c` MVP-1 freeze v1.0（T1 神谕封存 + 协议 + 冻结日志）
- `2f3453c` fix: repo_frozen 以真实内容入库（原 gitlink 不可审计）+ tar 备份
  （`repo_frozen_freeze.tar.gz`，sha256 前 16 位 `4ec5ddc25b83f093`）
- `12ee145` docs: README 状态
- 内层原始快照哈希（历史记录）：`a0891da4568dd2eb4ca1bd056fe56845bc5af8eb`

## T3 冻结（D-003，2026-10-09 03:55）

- 裁决依据：D-003（立即冻结，不等 E/T2 运行结果；轮次参数字段=跟随 MVP-1
  协议届时生效版本；与 T1 同规格验证；运行排序在第二轮与 T2 之后）
- 冻结内容：`tasks/T3/task.md`（惯例探针任务文本——请求不指定列名/列位/
  涉及表，合成请求显式标注）+ `tasks/T3/oracle/hidden/`（spec-direct 5 +
  edge 3）+ oracle 侧 fixture 副本（与冻结 repro 逐字节一致，sha256：
  access.log `b79b16e5…`、combined.log `954d2b1c…`、nginx.conf
  `9819a2ec…`、nginx_multiline.conf `8873f229…`）+ `expected_stats.md`
  （手算值）+ `PROVENANCE.md`（冻结时随附分类）
- 冻结前验证（D-003(2) 同规格）：
  1. 基线绿：repo_frozen 存量 28/28 通过（冻结前复验）
  2. 神谕红绿逻辑：未改动仓库 spec-direct 5 红 / edge 3 绿；实验者原型
     实现（CTE 窗口函数，封存件内详述）8/8 绿
  3. relevant-files 机械推导（下方）
  4. 盲化规则：惯例分析封存件 `tasks/T3/convention_analysis_SEALED.md`
     于神谕与冻结之后单独提交（git 提交顺序=写入顺序证明）；task.md/
     oracle/相关文件清单均不引用其内容
- 与 T1 的两处差异（如实记录）：(a) oracle 断言用 oracle 侧 fixture 副本
  调用 CLI，较 T1（读 agent 工作副本 repro/）加固防篡改；(b) PROVENANCE
  于冻结时随附（T1 为冻结后审计补做）
- 冻结 commit：`7ff9310`（主体）+ 本文件更新 commit（见 git log）

## T3 relevant-files 推导（侦察覆盖率分母，防反推收窄）

推导规则（机械，先于清单）：任务文本引用的公开行为面（默认报表输出、
bytes_sent 统计、平均值并见）+ 承载这些面的实现文件 + 覆盖这些面的既有
测试与文档。

清单（4 项）：
1. `ngxtop/ngxtop.py`（CLI 入口、DEFAULT_QUERIES、查询执行与输出）
2. `README.rst`（默认报表公开文档面，含输出样例）
3. `tests/test_characterization.py`（钉默认输出行为的既有特征化测试）
4. `tests/test_parse_log.py`（日志解析/字段面既有测试参考）

自检：实验者参考实现仅改动 ngxtop/ngxtop.py；本清单宽于实现所需
（README 与两项测试按规格面规则保留），不存在收窄偏置。

## T3 运行排序（D-003(3)）

第二轮@30 之后、在 T2 运行之后（与 T2 排序以届时执行序列为准）。

## T1 神谕修正（D-008，2026-10-09 05:10 裁决）

- 修正：tasks/T1/oracle/hidden/test_t1_hidden.py 的 summary_row()——
  数据行判据（| 起始且首列数值），锚定 docstring 原意；断言与期望值
  零改动；仅此一处
- 冻结时缺陷：绿路径下误取 orgtbl 表头行（2xx…5xx→[2,3,4,5]）→
  spec#1 对任何正确实现恒假红；冻结验证只跑红侧故漏网（教训已升格
  PROTOCOL v1.1 追加条款：冻结验证必须含绿侧）
- 复验三件（全档 runs/E/integration-records/post-d008/）：红侧 5R/3G
  与冻结一致；参考修复 8/8；存量 28/28 双仓。加跑：验收器于参考修复
  首达 ACCEPTANCE PASS（E 反馈环闭合）
- 替代关系：冻结 commit 34f1d8c 的该函数实现（D-008 授权，修正 commit
  见 git log 本条；PROVENANCE.md 修正条目在案）

