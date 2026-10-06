# fixture 手算期望值（T1 oracle 依据，冻结件）

## repro/access.log（issue #108 格式，5 行）

| 行 | request_path | status | bytes_sent |
|----|--------------|--------|------------|
| 1  | /            | 200    | 5120       |
| 2  | /api         | 404    | 153        |
| 3  | /            | 200    | 2048       |
| 4  | /img/a.png   | 500    | 512        |
| 5  | /old         | 301    | 300        |

派生量：
- count = 5
- avg_bytes_sent = (5120+153+2048+512+300)/5 = 8133/5 = **1626.6**
- 2xx = 2（行1、行3），3xx = 1（行5），4xx = 1（行2），5xx = 1（行4）
- 默认分组（request_path）：`/` 计数 2；`/api`、`/img/a.png`、`/old` 各 1

## repro/combined.log（默认 combined 格式，2 行）

- count = 2；status 200/404；bytes 5120/153；avg = 2636.5

## 已知冻结前实测（供审计对照）

- 直传 ISSUE_FMT 格式串 + access.log → 5 records，stats 与上表一致
- `-f main -c nginx.conf -l access.log` → 0 records（issue #108 症状复现）
- config_parser.get_log_formats 对单行/多行定义均解析出完整格式串（冻结前验证）
