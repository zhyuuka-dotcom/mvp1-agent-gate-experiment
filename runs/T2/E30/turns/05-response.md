The citation format requires `path:start-end | quote`. Let me get exact lines to quote correctly.

RUN grep -n "import argparse" ngxtop/config_parser.py && grep -n "records processed" ngxtop/ngxtop.py

Let me capture exact full lines.

RUN sed -n '1,3p' ngxtop/config_parser.py | cat -A | head -5

RUN sed -n '1,3p' ngxtop/ngxtop.py | cat -A | head -5

Let me get the exact quote lines without trailing issues.

RUN awk 'NR==1{print "CP1:"$0}' ngxtop/config_parser.py; awk 'NR==1{print "NG1:"$0}' ngxtop/ngxtop.py

Let me find good quotable lines.

RUN grep -n "records processed" ngxtop/ngxtop.py

Let me look at exact content of that line.

RUN awk 'NR==300' ngxtop/ngxtop.py | cat -A

Let me find the exact status-line print line.

RUN grep -n "records processed" ngxtop/ngxtop.py && awk 'NR==301' ngxtop/ngxtop.py

Let me just get clean single lines.

RUN sed -n '301p' ngxtop/ngxtop.py

Hmm, let me search more precisely.

RUN grep -n "processed\|running for\|stderr\|print" ngxtop/ngxtop.py | head -30

Now I have exact line numbers. Let me get the exact text of some lines.

RUN awk 'NR==1' ngxtop/config_parser.py; echo "---"; awk 'NR==2' ngxtop/config_parser.py; echo "---"; awk 'NR==1' ngxtop/ngxtop.py; echo "---"; awk 'NR==2' ngxtop/ngxtop.py

Now I'll craft the plan with the exact format: `path:start-end | exact line`.

WRITE PLAN.md
<<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/config_parser.py
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: CLI 选项在 config_parser.py 中集中定义，可直接新增一个选项
  依据: ngxtop/config_parser.py:1-1 | import argparse
  验证: 运行 CLI --help 查看新选项出现
- 假设: 报表状态行与表格由 ngxtop.py 打印
  依据: ngxtop/ngxtop.py:1-1 | import sys
  验证: 运行 CLI 观察 table 输出

## BEHAVIOR_DELTAS
- 增量: 新增 --output-format 选项，接受 table/json，默认 table
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json | .venv/bin/python -c 'import json,sys; json.load(sys.stdin)'
- 增量: json 模式 stdout 只输出一个 JSON 文档，状态行走 stderr
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json
- 增量: 非法取值报错并非 0 退出
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml; echo $?

## NON_GOALS
- 非目标: 不改变 table 模式输出
  GUARD: .venv/bin/python -m pytest tests/ -q

## TEST_PLAN
1. 先运行现有测试确认基线
2. 实现选项与 JSON 输出
3. 运行验收例 1/2/3 验证
4. 重跑全部测试
FILE_CONTENTS
