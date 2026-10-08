# T3 任务：输出增加 bytes_sent 中位数统计（惯例探针）

> 本文件是发给 Agent 的任务文本，三臂（A/C/E）逐字相同。
> 只含请求原文 + 复现材料说明 + 运行方式。请求未指定新增统计列的名称、位置、
> 应出现在哪些输出表中——未指定的取值以仓库公开证据为准。

## 背景

以下是本仓库（ngxtop，nginx 日志分析 CLI）的一个功能请求（为实验目的合成的
请求文本，非仓库真实 issue 归档）。你的任务：让请求反映的需求得到实现。

## 功能请求原文

**标题**：add median of bytes_sent to the report

**正文**：

> The default report shows the average of bytes_sent. But averages get
> skewed by outliers — one huge download makes every request look "big on
> average". Can ngxtop also report the median of bytes_sent in its output,
> so it's possible to see the typical request size next to the average?

## 本仓库复现材料（对所有运行者相同）

- `repro/nginx.conf` —— log_format main 定义的单行形式（nginx 配置语法）
- `repro/nginx_multiline.conf` —— 同一定义的原始多行形式
- `repro/access.log` —— 匹配该格式的日志样本（5 行）
- `repro/combined.log` —— 默认 combined 格式的日志样本（2 行）

## 运行方式

- 运行 CLI：`.venv/bin/python -m ngxtop.ngxtop <参数>`
- 运行全部测试：`.venv/bin/python -m pytest tests/ -q`

## 完成标准

按本实验通用协议声明完成（协议由 harness 在运行时提供）。
