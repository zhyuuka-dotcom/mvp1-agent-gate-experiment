# COVERAGE｜任务 csv-export 覆盖表（研究工件，冻结）

> 对 agent 不可见（S7）；冻结 2026-10-10；对应 oracle.py TESTS 映射

| 要求句柄 | 内容 | 测试 | agent 可见？ |
|---|---|---|---|
| RE-1 | --csv 开关存在（docopt 参数化） | T_spec_1 | 明示 |
| RE-2 | 列头=表列序（逗号分隔） | T_spec_1 | 明示 |
| RE-3 | Summary 数值与人类模式一致 | T_spec_2 | 明示 |
| RE-4 | 无 --csv 零回归（基线逐字节） | T_spec_3 | 明示 |
| EC-1 | 空数据边界（count=0 行如实，不出非零行） | T_edge_1 | 隐藏 |
| EC-2 | 参数兼容（--csv × --no-follow） | T_compat_1 | 隐藏 |
| EC-3 | CSV 转义（含逗号字段 RFC 4180 引号） | T_hidden_1 | 隐藏 |
| EC-4 | follow 流式模式下的 CSV 行为 | （无覆盖） | 隐藏 |
| EC-5 | --csv × --print-resolv 等其他参数组合 | （无覆盖） | 隐藏 |

覆盖缺口（无覆盖条款）：EC-4、EC-5——验收套件不测，随结果
注记披露（verified ≠ 满足全部规格）。

类别 taxonomy（四类，用于隐藏反馈标签）：EC-1=边界（BOUNDARY）；
EC-2=兼容（COMPAT）；EC-3=错误处理（ERR-HANDLING：转义属输出
正确性）；EC-4=兼容；EC-5=兼容。
