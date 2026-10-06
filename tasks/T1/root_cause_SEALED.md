# T1 根因分析（SEALED — 封存件）

> 封存规则（对应对话裁决 2026-10-06）：
> 1. 本文件在隐藏测试与特征化测试**之后**写入（审计轨迹见 git 提交顺序）
> 2. task.md、hidden tests、characterization tests、relevant-files 清单
>    均不得引用本文件内容
> 3. 本文件仅在实验结束后的分析阶段解封，用于对照 Agent 的侦察/修复路径
> 4. 若 Agent 的有效修复与本分析不一致，以 Agent 实测为准——本分析可能不完整

## 假设→验证→修正轨迹（实验者自己的，保留供方法论审计）

- **H1（初判，错误）**：config_parser 无法解析多行 log_format 定义（引号续行断裂）。
  对照实验：单行命名的 `main2` + `-l` 同样 0 条 → H1 被推翻。
- **H2（debug 模式 + 代码阅读，确认）**：`-f <名字>` 的解析路径在任何分支都不存在：
  - `ngxtop.py process()`（~L580-587）：`log_format = arguments['--log-format']`
    被直接当**字面格式串**用于 `build_pattern()`；只有 `access_log is None`
    （即未给 `-l`）时才调用 `detect_log_config()`，而该函数**完全无视 `-f`**，
    返回配置文件自身的 access_log+格式。
  - `config_parser.get_log_formats()` 本身工作正常：对单行/多行定义都正确
    拼接出完整格式串（冻结前直接调用验证，见 expected_stats.md 末节）。
- **结论**：issue #108 的根因 = 「`-l` 在场时 `-f` 的值不作为格式名解析」，
  病灶集中在 `process()` 的参数分派，config_parser 无辜。

## 预期修复形态（仅供赛后对照，非规格）

`process()` 中：`-l` 在场且 `-f` 值不含 `$`（非格式串形态）时，从 `-c`/自动探测
的配置解析该名字；未找到 → 干净报错（与 detect_log_config 现有 error_exit 惯例一致）。

## 与神谕的独立性自检

- hidden spec-direct 断言只依赖 issue 原文（命令、症状、期望"有结果行"）与
  fixture 手算值——不涉及 process()/config_parser 的任何内部结构
- hidden edge 三条钉的是"直传格式串/默认 combined/配置探测路径"三个公开行为，
  在修复前即为绿（保持类），其选取依据是 README/docopt 文档面，非根因
- relevant-files 清单由规格面机械推导（见 freeze_log.md），包含 config_parser.py
  ——比根因所指的文件**更宽**，不存在按根因收窄的情况
