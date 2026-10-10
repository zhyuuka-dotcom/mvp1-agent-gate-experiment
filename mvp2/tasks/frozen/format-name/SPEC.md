# SPEC.md｜任务 format-name（agent 可见规格文本，冻结）

> 冻结：2026-10-11（D-022 §3(b)）；sha256 见 MANIFEST.sha256
> 版本：v1.0-frozen

## 任务：让 -f/--log-format 支持"格式名引用"

功能规格：

1. `-f main`（名字）：在 `--config`（-c）指定的 nginx 配置文件
   的 `log_format` 指令中查名字 `main`，用其定义串做字段解析
   （行为等价于直接给格式串）。
2. `-f` 仍是格式串时（含 `$` 变量）：行为与现状一致（零回归）。
3. `-f <名字>` 在配置中不存在：报错信息含 `unknown format name`，
   退出码非零。

验收例（逐值；输入数据可读：<DATA_DIR>/access.log 共 5 条记录；
<DATA_DIR>/base.conf 含标准 main 定义；<DATA_DIR>/dup.conf 含
两个同名 main；<DATA_DIR>/quoted.conf 含带引号名 'my format'）：

- `-l <DATA_DIR>/access.log -c <DATA_DIR>/base.conf -f main
  --no-follow`：Summary 数值 == `-f '<main 定义串>'` 同输入
- `-f '<格式串>'`（含 $ 变量）：与基线逐字节一致（零回归）
- `-f nosuchname -c <DATA_DIR>/base.conf`：stderr 含
  `unknown format name`，rc != 0
- `-f main -c <DATA_DIR>/dup.conf`：数值等于取**首个** main
  定义（等效于直接给首个定义串）
- `-f "my format" -c <DATA_DIR>/quoted.conf`：数值等于直接给
  该定义串
- `-f Main -c <DATA_DIR>/base.conf`：报错（大小写敏感）

## mechanics 基座条款（v1.0 §0/§1/§2）

按 mvp2/MECHANICS.md v1.0（裸 A 基线：无门禁/无审计条款）。
