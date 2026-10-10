# COVERAGE｜任务 top-n 覆盖表（研究工件，冻结）

> 对 agent 不可见（S7）；冻结 2026-10-11；对应 oracle.py TESTS 映射

| 要求句柄 | 内容 | 测试 | agent 可见？ |
|---|---|---|---|
| RE-1 | --top N 截断 Detailed 前 N 行（首行不变） | T_spec_1 | 明示 |
| RE-2 | 无 --top 零回归（含 -n 现状） | T_spec_2 | 明示 |
| RE-3 | --top 0 仅表头（Summary 照常） | T_spec_3 | 明示 |
| EC-1 | N ≥ 总行数 → 全量 | T_edge_1 | 隐藏 |
| EC-2 | 超大值健壮（2147483647） | T_edge_2 | 隐藏 |
| EC-3 | 非整数 → 参数层报错（非 SQL 崩溃） | T_hidden_1 | 隐藏 |
| EC-4 | 负数 → 参数层报错 | T_hidden_2 | 隐藏 |
| EC-5 | --top × -n 组合优先级（--top 优先） | T_compat_1 | 隐藏 |
| EC-6 | --top × follow 流式行为 | （无覆盖） | 隐藏 |

覆盖缺口：EC-6（注记披露）。

**负向验证口径登记（冻结）**：未实现态下 T_spec_2（零回归）与
T_hidden_1/2（参数校验暗区）天然无区分力（未实现=rc!=0 或
零回归恒过）——暗区断言测"实现存在时的校验形态"，负向必挂集
= 功能断言（T_spec_1/3、T_edge_1/2、T_compat_1）共 5 项。

类别 taxonomy：EC-1=边界；EC-2=边界；EC-3=错误处理；EC-4=
错误处理；EC-5=兼容；EC-6=兼容。
