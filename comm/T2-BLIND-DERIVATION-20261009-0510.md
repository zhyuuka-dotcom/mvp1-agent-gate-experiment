# T2 盲推导清单 — GLM-5.3（D-006 盲方产物）存档

> 时间戳边界：本 commit = D-006 硬序边界——本清单存档后，推导方才可读
> T2 神谕。以下为指令原文 §四 逐字（源：comm/PI-20261009-0510.md L25-45）。

四、T2 盲推导清单（D-006 盲方产物）
声明：本清单仅依据 tasks/T2/task.md 推导（另查阅了仓库文件目录名，属协议允许的信息）。我尚未接触 T2 神谕、fixtures、spec_notes 任何内容。清单存档后我才读神谕做匹配审计。
验收点（每项含文本依据引文）
1. 默认 table：不传选项时 stdout 含 Summary: orgtbl 表、整体非单一 JSON 文档。〔引文："缺省（不传该选项时）为 table"〕
2. 显式 table ≡ 缺省：--output-format table 与不传，stdout 逐字节相同、退出码相同。〔引文："显式传 --output-format table 与不传的行为完全相同"〕
3. table 模式布局不变：stdout 中状态行（running for … records processed 形态）先于 Summary:，Summary 与 Detailed 两表俱在。〔引文："stdout 先打印状态行…随后是 Summary 与 Detailed 两张 orgtbl 表；不引入任何格式变化"〕
4. json 纯度：json 模式 stdout 经 json.loads 解析成功且仅此一文档。〔引文："stdout 恰好包含一个合法 JSON 文档（json.loads 可解析），除该文档外不含任何其他字符"〕
5. json 模式状态行走 stderr 且计数一致：stderr 含状态行形态与 N records processed，N 与 table 模式状态行计数相同。〔引文："状态行走 stderr（内容与 table 模式的状态行相同）"〕
6. 顶层键恰为 {"summary","detailed"}。〔引文："顶层对象恰有两个键"〕
7. summary 键集 = {count, avgbytessent, 2xx, 3xx, 4xx, 5xx}。〔引文：§4 summary 条目〕
8. summary 值类型：count/2xx/3xx/4xx/5xx 为整数（bool 不算），avgbytessent 为数值。〔引文："count/2xx/3xx/4xx/5xx 为整数，avgbytessent 为数值"〕
9. detailed 元素：默认分组下每元素键 = {requestpath} ∪ 上列 6 统计列；requestpath 为字符串、统计列为数值。〔引文："键为分组列名（默认 request_path）加上与 summary 相同的统计列名"〕
10. 例 1 全值：combined.log json 运行，summary = {count 2, avg 2636.5, 2xx 1, 3xx 0, 4xx 1, 5xx 0}；detailed = /api{1, 153.0, 0,0,1,0} 与 /{1, 5120.0, 1,0,0,0} 两行（行序无关、数值相等即可）。〔引文：验收例 1 全块〕
11. 例 1 stderr 含 2 records processed。〔引文：例 1 stderr 行〕
12. 例 2 全值：ISSUE_FMT 直传 + access.log json 运行，summary = {count 5, avg 1626.6, 2xx 2, 3xx 1, 4xx 1, 5xx 1}；detailed 四行 /、/old、/img/a.png、/api 按例 2 数值（行序无关）。〔引文：验收例 2 全块〕
13. 例 2 stderr 含 5 records processed。〔引文：例 2 stderr 行〕
14. 非法取值：--output-format yaml → 退出码非 0、stderr 有错误信息、stdout 无 JSON。〔引文："stderr 输出一行错误信息，退出码非 0，stdout 不输出 JSON" + 例 3〕
15. 存量测试全绿：pytest tests/ 28 条通过。〔引文："仓库既有测试（pytest tests/，28 条）必须全部保持通过"〕
16. 〔边界推导，是否入神谕由匹配审计判〕不设短别名：-o json 不得产生 json 输出。〔引文："只有长名，不设短别名；-o 已被 --order-by 占用"〕
显式排除（有引文支持的不作要求项，不入验收）：子命令 × --output-format 组合〔引文："维持现状即可，不作要求"〕。
方法注记：数值比较按"数值相等即相等"（5120≡5120.0）；键序/行序不敏感；我手核了两例内部算术自洽（例 2：7168+300+512+153=8133，8133/5=1626.6 ✓），例值可作确定性检查基准。
