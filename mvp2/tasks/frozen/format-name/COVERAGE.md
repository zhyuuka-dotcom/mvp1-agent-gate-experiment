# COVERAGE｜任务 format-name 覆盖表（研究工件，冻结）

> 对 agent 不可见（S7）；冻结 2026-10-11；对应 oracle.py TESTS 映射

| 要求句柄 | 内容 | 测试 | agent 可见？ |
|---|---|---|---|
| RE-1 | -f 名字 → log_format 定义解析（数值等价） | T_spec_1 | 明示 |
| RE-2 | -f 格式串直传零回归 | T_spec_2 | 明示 |
| RE-3 | 未知名报错（unknown format name + rc≠0） | T_spec_3 | 明示 |
| EC-1 | 同名 log_format 歧义 → **取首个** | T_edge_1 | 隐藏 |
| EC-2 | 带引号名（'my format'）匹配 | T_edge_2 | 隐藏 |
| EC-3 | 名解析 × --no-follow 兼容 | T_compat_1 | 隐藏 |
| EC-4 | 名字大小写敏感（Main≠main） | T_hidden_1 | 隐藏 |
| EC-5 | 非--config 路径下名解析行为（conf 未提供/不存在） | （无覆盖） | 隐藏 |
| EC-6 | 保留名 combined/common/caddy 与自定义名冲突 | （无覆盖） | 隐藏 |

覆盖缺口：EC-5、EC-6（注记披露于结果；EC-6 提示：内置保留名
优先于名解析——任务验收例避开保留名）。

类别 taxonomy：EC-1=分组（GROUPING：同名指令歧义）；EC-2=兼容
（COMPAT：nginx 引号语法）；EC-3=兼容；EC-4=边界（BOUNDARY：
大小写）；EC-5=错误处理；EC-6=兼容。
