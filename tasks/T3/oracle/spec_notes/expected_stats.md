# fixture 手算期望值（T3 oracle 依据，冻结件）

## repro/access.log（issue 格式，5 行；oracle 侧副本逐字节同）

| 行 | request_path | status | bytes_sent |
|----|--------------|--------|------------|
| 1  | /            | 200    | 5120       |
| 2  | /api         | 404    | 153        |
| 3  | /            | 200    | 2048       |
| 4  | /img/a.png   | 500    | 512        |
| 5  | /old         | 301    | 300        |

全表中位数（排序 153,300,**512**,2048,5120）= **512**

按 request_path 分组中位数：
- `/`（2 行：5120,2048 → 排序 2048,5120 → (2048+5120)/2）= **3584**
- `/api`（1 行）= **153**
- `/img/a.png`（1 行）= **512**
- `/old`（1 行）= **300**

其他派生量（edge 断言用）：
- count = 5；avg_bytes_sent = 8133/5 = 1626.6
- 2xx = 2（行1、行3）、3xx = 1（行5）、4xx = 1（行2）、5xx = 1（行4）
- Detailed 分组行：`/` count=2；`/old`、`/img/a.png`、`/api` 各 count=1

## repro/combined.log（默认 combined 格式，2 行）

- 行 1：request_path=`/`，status 200，bytes 5120
- 行 2：request_path=`/api`，status 404，bytes 153

全表中位数（153,5120 → (153+5120)/2）= **2636.5**
按 request_path 分组中位数：`/` = **5120**；`/api` = **153**
avg_bytes_sent = 2636.5；2xx=1、4xx=1

## 冻结前实测（供审计对照，原型验证时记录）

- 未改动仓库：两表均无 median_bytes_sent（spec-direct 五红）；avg/状态列/
  分组行为与上表一致（edge 三绿）
- 原型实现（CTE 窗口函数，见 convention_analysis_SEALED.md）后：八绿
- 直传 FMT_MAIN + access.log → 5 records processed（与 T1 oracle 同源公开
  行为）；默认 combined → 2 records processed
