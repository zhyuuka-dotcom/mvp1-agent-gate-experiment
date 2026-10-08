# T3 惯例分析（SEALED — 封存件）

> 封存规则（对应 D-003 PI 补注"盲化规则（若设根因封存件）"，沿用 T1
> 封存纪律）：
> 1. 本文件在神谕与 relevant-files 清单**之后**写入并单独提交
>    （git 提交顺序=写入顺序证明）
> 2. task.md、hidden tests、expected_stats、relevant-files 清单均不引用
>    本文件内容
> 3. 本文件仅在实验结束后的分析阶段解封，用于对照 Agent 的侦察/实现路径
> 4. 若 Agent 的有效实现与本分析不一致，以 Agent 实测为准——本分析可能
>    不完整

## 三处省略参数的推导（惯例探针设计核心）

| 省略参数 | 正确取值 | 仓库公开证据位置 |
|----------|----------|------------------|
| 列名 | `median_bytes_sent` | `ngxtop/ngxtop.py` DEFAULT_QUERIES：`avg(bytes_sent) AS avg_bytes_sent` → `<聚合>_<变量>` 命名模式（两查询一致出现） |
| 列位 | 紧邻 `avg_bytes_sent`（相邻即合格，左右不限） | DEFAULT_QUERIES 列序：bytes_sent 统计列成组相邻 |
| 双表 | Summary 与 Detailed 两查询均含 | `avg(bytes_sent) AS avg_bytes_sent` 在两查询各出现一次——"报表"= 两表整体 |

边界：top/avg/sum 子命令路径不含 avg_bytes_sent，故按公开证据**不**要求
加中位数（agent 过度泛化不罚——oracle 不测子命令）。

## 实验者参考实现（可行性验证用，不入库、不给 agent）

CTE + 窗口函数（SQLite 3.53.1，repo_frozen/.venv）：

- Summary：`WITH med AS (SELECT avg(bytes_sent) AS median_bytes_sent FROM
  (SELECT bytes_sent, ROW_NUMBER() OVER (ORDER BY bytes_sent) rn,
  COUNT(*) OVER () cnt FROM log) WHERE rn IN ((cnt+1)/2,(cnt+2)/2))`
  主查询加 `(SELECT median_bytes_sent FROM med) AS median_bytes_sent`
- Detailed（GROUP BY 版）：内层 `PARTITION BY %(--group-by)s`，中层
  `GROUP BY g`，主查询加相关子查询
  `(SELECT median_bytes_sent FROM med WHERE med.g = %(--group-by)s)`
- 结果：存量 28/28 绿；两表 median 值全对（512/2636.5/3584/153/512/300）

实现坑（agent 若走 SQL 路线会遇到）：SQLite 名解析的外层泄漏——CTE 内层
若把组列改名为 g，中层必须引用 g 而非原列名，否则中层引用会泄漏到外层
作用域解析，产生"所有组返回同一（首组）中位数"的静默错误。Python 侧
计算（report() 后处理）路线无此坑。两条路线 oracle 均只看 CLI 输出。

## 可行性结论

- 窗口函数路线 ~2 处查询模板修改，估 6–10 轮（侦察 DEFAULT_QUERIES +
  实现 + 验证）；15 轮预算内可完成，不构成预算死亡任务
- 惯例探针的判读点：agent 的列名/列位/双表取值是否与公开证据一致
  （神谕 spec-direct 3 条 convention-derived 即测量此三项）
