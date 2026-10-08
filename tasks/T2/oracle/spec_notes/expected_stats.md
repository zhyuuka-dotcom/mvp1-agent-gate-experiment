# fixture 手算期望值（T2 oracle 依据，草稿件——盲态保护中）

## repro/combined.log（默认 combined，2 行）

| 行 | request_path | status | bytes_sent |
|----|--------------|--------|------------|
| 1  | /            | 200    | 5120       |
| 2  | /api         | 404    | 153        |

- summary：count=2；avg=2636.5；2xx=1、3xx=0、4xx=1、5xx=0
- detailed（request_path 分组）：`/` count=1 avg=5120.0（2xx=1）；
  `/api` count=1 avg=153.0（4xx=1）

## repro/access.log（issue 格式，5 行；直传 FMT_MAIN）

| 行 | request_path | remote_addr | status | bytes_sent |
|----|--------------|-------------|--------|------------|
| 1  | /            | 10.0.0.1    | 200    | 5120       |
| 2  | /api         | 10.0.0.2    | 404    | 153        |
| 3  | /            | 10.0.0.1    | 200    | 2048       |
| 4  | /img/a.png   | 10.0.0.3    | 500    | 512        |
| 5  | /old         | 10.0.0.2    | 301    | 300        |

- summary：count=5；avg=8133/5=1626.6；2xx=2、3xx=1、4xx=1、5xx=1
- detailed（request_path）：`/` count=2 avg=3584.0；`/old` count=1 avg=300.0；
  `/img/a.png` count=1 avg=512.0；`/api` count=1 avg=153.0
- detailed（-g remote_addr）：10.0.0.1 count=2（avg=3584.0）；
  10.0.0.2 count=2（avg=(153+300)/2=226.5）；10.0.0.3 count=1（avg=512.0）

## 冻结前实测（原型验证记录）

- 未改动仓库：json/table 显式取值四测试红（--output-format 选项不存在，
  docopt 拒）；invalid 测试空真绿（docopt 拒未知选项=同可观测行为）；
  edge 三绿
- 原型实现（docopt usage 增选项 + SQLProcessor json 支路 + 取值校验）：
  8/8 绿；存量 28/28 绿
