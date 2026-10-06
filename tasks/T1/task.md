# T1 任务：命名日志格式无法解析（真实 issue #108）

> 本文件是发给 Agent 的任务文本，三臂（A/C/E）逐字相同。
> 只含 issue 原文 + 复现材料说明 + 运行方式。无根因、无修复方向提示。

## 背景

以下是本仓库（ngxtop，nginx 日志分析 CLI）的一个真实用户报告。你的任务：让报告反映的问题得到解决。

## 用户报告原文（issue #108）

**标题**：i have nginx format but not show any result line

**正文**：

```
log_format  main  '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] '
                  '$host "$request" $status $bytes_sent '
                  '"$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"';

/usr/local/python3.9/bin/ngxtop  -f main -l /var/log/nginx/access.log --no-follow
```

（即：用户在 nginx 配置中定义了名为 `main` 的 log_format，用 `-f main` 指定该格式运行，得不到任何结果行。）

## 本仓库复现材料（对所有运行者相同）

- `repro/nginx.conf` —— 报告中 log_format main 定义的单行形式（nginx 配置语法）
- `repro/nginx_multiline.conf` —— 报告原文的原始多行形式
- `repro/access.log` —— 匹配该格式的日志样本（5 行）
- `repro/combined.log` —— 默认 combined 格式的日志样本（2 行）

## 运行方式

- 运行 CLI：`.venv/bin/python -m ngxtop.ngxtop <参数>`
- 运行全部测试：`.venv/bin/python -m pytest tests/ -q`

## 完成标准

按本实验通用协议声明完成（协议由 harness 在运行时提供）。
