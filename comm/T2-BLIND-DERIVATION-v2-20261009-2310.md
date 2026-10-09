# T2 盲推导清单 v2 — D-009 修订轮（推导者：deepseek-flash）存档

> **时间戳边界**：本 commit = D-009 复审计硬序边界——本清单存档后 PI 复审计（口径：测试级、语义等价或更强、≥90%）。

> **推导者身份（全透明披露）**：deepseek-flash，经 learnhub/bin/ds-agent.sh 全新会话（零项目上下文、不携带任何历史，无 -c conv 文件），用户 2026-10-09 23:09 指定使用（"你不是有deepseek吗"= D-009"由用户组织新推导"的执行）。flash 未参与 T2 文本/神谕撰写、未运行过 T2（六臂运行均为 T1），盲态成立。
> **防操纵披露**：prompt 为中性指令 + tasks/T2/task.md（v2）全文，一字不差归档于下；无任何验收点提示、无边界项提示。执行者（神谕作者）仅作仪器操作员。PI 复审计时如裁定推导者身份不合格，本清单作废重推，本档保留不删。
> **元信息**：flash / thinking disabled / in 1824 tok / out 1331 tok / ~$0.00107（谷段）

---

## 推导输出（flash 原文，一字未改）

# 验收检查点清单

1. `--output-format` 选项存在且仅接受长名（无短别名，不占用 `-o`）。〔依据："新增选项 `--output-format <fmt>`（只有长名，不设短别名；`-o` 已被 `--order-by` 占用）"〕
2. 缺省不传该选项时行为为 table，显式传 `--output-format table` 与不传完全相同。〔依据："合法取值为 `table` 与 `json`；缺省（不传该选项时）为 `table`。显式传 `--output-format table` 与不传的行为完全相同。"〕
3. table 模式输出与现行版本一致：stdout 先状态行，随后 Summary 与 Detailed 两张 orgtbl 表，无格式变化。〔依据："table 模式：输出与现行版本完全相同——stdout 先打印状态行…随后是 Summary 与 Detailed 两张 orgtbl 表；不引入任何格式变化。"〕
4. json 模式 stdout 恰好为一个合法 JSON 文档（`json.loads` 可解析），无其他字符。〔依据："stdout 恰好包含一个合法 JSON 文档（json.loads 可解析），除该文档外不含任何其他字符"〕
5. json 模式状态行走 stderr，内容与 table 模式状态行相同。〔依据："状态行走 stderr（内容与 table 模式的状态行相同）；"〕
6. JSON 顶层对象恰有 `"summary"` 与 `"detailed"` 两个键。〔依据："顶层对象恰有两个键 `"summary"` 与 `"detailed"`"〕
7. `"summary"` 为对象，键为 `count`、`avg_bytes_sent`、`2xx`、`3xx`、`4xx`、`5xx`，值为数值类型（计数字段整数，avg_bytes_sent 数值）。〔依据："`"summary"`：一个对象，键为 Summary 查询的列名（`count`、`avg_bytes_sent`、`2xx`、`3xx`、`4xx`、`5xx`），值为数值类型…"〕
8. `"detailed"` 为数组，每元素对象含分组列名（默认 `request_path`）加相同统计列名；分组列为字符串，统计列为数值。〔依据："`"detailed"`：一个数组，每个元素为一个对象…键为分组列名（默认 `request_path`）加上与 summary 相同的统计列名；分组列的值为字符串，统计列为数值类型。"〕
9. 键序、detailed 行序不作要求，数值相等即相等（如 `5120` 与 `5120.0`）。〔依据："键序不作要求；`"detailed"` 的行序不作要求…数值相等即相等（如 `5120` 与 `5120.0`）。"〕
10. 例 1 通过：combined.log + json 输出指定 summary/detailed 值，stderr 含 `2 records processed`。〔依据："例 1…stdout（一个 JSON 文档…）：…stderr：状态行（含 `2 records processed`）。"〕
11. 例 2 通过：access.log + 直传格式串 + json 输出指定 summary/detailed 值，stderr 含 `5 records processed`。〔依据："例 2…stdout（同上比较规则）：…stderr：状态行（含 `5 records processed`）。"〕
12. 非法取值（如 `yaml`）时退出码非 0，stderr 一行错误信息，stdout 无 JSON。〔依据："非法取值…`yaml`：stderr 输出一行错误信息，退出码非 0，stdout 不输出 JSON。"与例 3〕
13. 既有 28 条测试（`pytest tests/`）全部保持通过。〔依据："存量行为：仓库既有测试（`pytest tests/`，28 条）必须全部保持通过。"〕
14. `-g` 分组能力不回归：含多列分组（如 `-g remote_addr,status`）与直传格式串组合下默认报表仍正常输出。〔依据："分组能力回归：仓库既有的 `-g` 分组能力不得回归——默认报表在 `-g`（含多列分组…）与直传格式串组合下仍须正常输出"〕
15. JSON 模式下 `"detailed"` 元素键随分组列名变化（如 `-g remote_addr` 时含 `remote_addr`）。〔依据："JSON 模式下 `"detailed"` 元素的键随分组列名（如 `-g remote_addr` 时行对象键含 `remote_addr`）。"〕

## 规格未覆盖、但实际验收可能需要的边界项

- json 模式下 `-g` 多列分组的 JSON 键具体形态与值（如 `-g remote_addr,status` 时 detailed 行键的具体组合）未给出验收例，可能与单列分组行为一致与否需推断。
- `--output-format` 与子命令（top/avg/sum/query）组合时是否应被忽略或报错——规格明确"不作要求"，但验收可能仍会触发。
- 非法取值错误信息的确切措辞、是否需以特定前缀/格式打印——仅要求"一行错误信息"。
- 大小写敏感性（如 `JSON`、`Table`）规格未明确，仅说合法值为 `table`/`json`。
- `avg_bytes_sent` 在无数据或空 detailed 时的取值（如 `null` 与 0）未定义。
- 状态行 stderr 与 stdout 的刷新/顺序（是否有交错）在 json 模式下未明确。
- 传入 `--output-format` 后配合其他新选项（如 `--no-follow`、`-l`）的组合已在例中覆盖，但与其他未列组合未穷举。

---

## 推导 prompt（一字未改）

```
你将读到一份编程任务的完整规格文本。你的任务：仅依据这份文本本身（不假设任何外部信息、不请求查看任何代码库文件），推导出"验收此任务完成情况"的检查点清单。

规则：
- 每条一行，编号，格式：N. <检查点一句话>。〔依据："<规格原文引文>"〕
- 最多 15 条，按重要性排序
- 另外单列：你认为规格文本未覆盖、但实际验收可能需要的边界项（如有）

=== 任务规格全文开始 ===
# T2 任务：JSON 输出格式选项（完整规格）

> **本任务为 Benchmark-authored（规格由实验者撰写），非真实 issue。**
> 与真实 issue 任务不同：本任务规格完整，无省略参数——正确行为以本文件
> 规格与验收例为准，不需要从仓库惯例推断任何未指定取值。
> v2（D-009，2026-10-09）：增补规格 bullet 8（分组能力回归）——首轮盲推
> 7/8（87.5%）未达 90%，缺项为 -g 回归锚点，属文本可枚举项；神谕一字
> 不动，文本修订不涉既有 bullet。

## 背景

本仓库（ngxtop，nginx 日志分析 CLI）目前只以表格形式输出聚合报表。
脚本使用者希望拿到机器可读的结果。

## 规格

新增选项 `--output-format <fmt>`（只有长名，不设短别名；`-o` 已被
`--order-by` 占用），行为如下：

1. **取值与默认**：合法取值为 `table` 与 `json`；缺省（不传该选项时）
   为 `table`。显式传 `--output-format table` 与不传的行为完全相同。
2. **table 模式**：输出与现行版本完全相同——stdout 先打印状态行
   （`running for … seconds, N records processed: … req/sec`），随后是
   Summary 与 Detailed 两张 orgtbl 表；不引入任何格式变化。
3. **json 模式**：stdout 恰好包含一个合法 JSON 文档（json.loads 可解析），
   除该文档外不含任何其他字符；状态行走 stderr（内容与 table 模式的
   状态行相同）。
4. **JSON 结构**：顶层对象恰有两个键 `"summary"` 与 `"detailed"`：
   - `"summary"`：一个对象，键为 Summary 查询的列名（`count`、
     `avg_bytes_sent`、`2xx`、`3xx`、`4xx`、`5xx`），值为数值类型
     （count/2xx/3xx/4xx/5xx 为整数，avg_bytes_sent 为数值）；
   - `"detailed"`：一个数组，每个元素为一个对象，对应 Detailed 查询的
     一行；键为分组列名（默认 `request_path`）加上与 summary 相同的统计
     列名；分组列的值为字符串，统计列为数值类型。
   - 键序不作要求；`"detailed"` 的行序不作要求（按实现自然序）；
     数值相等即相等（如 `5120` 与 `5120.0`）。
5. **非法取值**：`--output-format` 传 table/json 之外的值（如 `yaml`）：
   stderr 输出一行错误信息，退出码非 0，stdout 不输出 JSON。
6. **范围**：本规格只约束默认报表（无子命令运行）的输出；子命令
   （top/avg/sum/query）与 `--output-format` 的组合行为不在本任务范围内
   （维持现状即可，不作要求）。
7. **存量行为**：仓库既有测试（`pytest tests/`，28 条）必须全部保持通过。
8. **分组能力回归**：仓库既有的 `-g` 分组能力不得回归——默认报表在
   `-g`（含多列分组，如 `-g remote_addr,status`）与直传格式串组合下
   仍须正常输出；JSON 模式下 `"detailed"` 元素的键随分组列名（如
   `-g remote_addr` 时行对象键含 `remote_addr`）。

## 验收例（fixture 与命令给全，期望输出逐值给出）

**例 1：combined.log + json（默认分组）**

```
.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json
```

stdout（一个 JSON 文档，键序/行序可不同，数值须相等）：

```json
{"summary": {"count": 2, "avg_bytes_sent": 2636.5, "2xx": 1, "3xx": 0, "4xx": 1, "5xx": 0},
 "detailed": [{"request_path": "/api", "count": 1, "avg_bytes_sent": 153.0, "2xx": 0, "3xx": 0, "4xx": 1, "5xx": 0},
              {"request_path": "/", "count": 1, "avg_bytes_sent": 5120.0, "2xx": 1, "3xx": 0, "4xx": 0, "5xx": 0}]}
```

stderr：状态行（含 `2 records processed`）。

**例 2：access.log（命名格式直传）+ json**

```
.venv/bin/python -m ngxtop.ngxtop -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' -l repro/access.log --no-follow --output-format json
```

stdout（同上比较规则）：

```json
{"summary": {"count": 5, "avg_bytes_sent": 1626.6, "2xx": 2, "3xx": 1, "4xx": 1, "5xx": 1},
 "detailed": [{"request_path": "/", "count": 2, "avg_bytes_sent": 3584.0, "2xx": 2, "3xx": 0, "4xx": 0, "5xx": 0},
              {"request_path": "/old", "count": 1, "avg_bytes_sent": 300.0, "2xx": 0, "3xx": 1, "4xx": 0, "5xx": 0},
              {"request_path": "/img/a.png", "count": 1, "avg_bytes_sent": 512.0, "2xx": 0, "3xx": 0, "4xx": 0, "5xx": 1},
              {"request_path": "/api", "count": 1, "avg_bytes_sent": 153.0, "2xx": 0, "3xx": 0, "4xx": 1, "5xx": 0}]}
```

stderr：状态行（含 `5 records processed`）。

**例 3：非法取值**

```
.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml
```

退出码非 0；stderr 一行错误信息；stdout 无 JSON。

## 本仓库复现材料（对所有运行者相同）

- `repro/nginx.conf`、`repro/nginx_multiline.conf`、`repro/access.log`（5 行）、
  `repro/combined.log`（2 行）——验收例数据源，内容固定

## 运行方式

- 运行 CLI：`.venv/bin/python -m ngxtop.ngxtop <参数>`
- 运行全部测试：`.venv/bin/python -m pytest tests/ -q`

## 完成标准

按本实验通用协议声明完成（协议由 harness 在运行时提供）。
=== 任务规格全文结束 ===
```
