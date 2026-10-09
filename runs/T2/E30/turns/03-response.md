Now I see the structure. The config module is `config_parser.py`, not `config.py`. Let me read the key files.

READ ngxtop/config_parser.py

Let me read the test files to understand testing conventions.

RUN for f in tests/test_*.py; do echo "=== $f ==="; head -30 "$f"; done

Let me look at the test files.

RUN wc -l tests/test_*.py

Let me read the characterization test which likely tests CLI output.

READ tests/test_characterization.py

Let me read more test files.

RUN head -50 tests/test_parse_log.py && echo "===" && head -40 tests/test_json_extraction_fix.py

Let me check the fixtures and how CLI is invoked in tests.

RUN grep -rn "ngxtop.ngxtop\|subprocess\|output-format\|--no-follow\|main(" tests/ | head -30

Let me verify my understanding of the report columns.

RUN grep -n "def main\|def setup_map\|def get_default_args\|def process\|order-by\|group-by\|--output" ngxtop/ngxtop.py

Now let me write the plan. First let me confirm the print output lines.

RUN grep -n "def \|print(\|print " ngxtop/ngxtop.py | head -50

Let me look at the report printing area precisely.

RUN awk 'NR>=340 && NR<=430 {print NR": "$0}' ngxtop/ngxtop.py

Let me view the remaining part of ngxtop.py.

RUN awk 'NR>=580 {print NR": "$0}' ngxtop/ngxtop.py

Let me read lines around 380-420 which contain main logic.

RUN awk 'NR>=560 && NR<=600 {print NR": "$0}' ngxtop/ngxtop.py

Now let me look at the option parsing.

RUN awk 'NR>=480 && NR<=560 {print NR": "$0}' ngxtop/ngxtop.py

Let me read the config_parser.py to understand option declarations.

READ ngxtop/config_parser.py

Now let me check the end of ngxtop.py where main() is.

RUN awk 'NR>=590 && NR<=625 {print NR": "$0}' ngxtop/ngxtop.py

Let me look at the last part.

RUN tail -60 ngxtop/ngxtop.py | cat -n

Let me get the total line count and final section.

RUN wc -l ngxtop/ngxtop.py && echo "---" && awk 'END{print NR}' ngxtop/ngxtop.py

Let me read the last 40 lines.

RUN awk 'NR>=580' ngxtop/ngxtop.py

Let me read the main() function.

RUN grep -n "def main\|__main__\|def process" ngxtop/ngxtop.py ngxtop/__init__.py ngxtop/config_parser.py

Let me read the end-of-file main.

RUN awk 'NR>=595' ngxtop/ngxtop.py

Let me check exact lines.

RUN awk 'END{print NR}' ngxtop/ngxtop.py && awk 'NR>=560 && NR<=600' ngxtop/ngxtop.py

Let me read the whole tail.

RUN awk 'NR>=600' ngxtop/ngxtop.py

Let me read lines 560-620.

RUN awk 'NR>=560' ngxtop/ngxtop.py

Let me read the file from 540.

RUN awk 'NR>=540' ngxtop/ngxtop.py

Hmm the file must be shorter. Let me check.

RUN wc -l ngxtop/ngxtop.py

Let me read lines 500-583.

RUN awk 'NR>=500' ngxtop/ngxtop.py

Now let me read the earlier portion with main/report.

RUN grep -n "def " ngxtop/ngxtop.py

Let me read the report and print_something functions.

RUN awk 'NR>=430 && NR<=500' ngxtop/ngxtop.py

Now I have a clear picture. Let me read the very specific area of table printing and status.

RUN awk 'NR>=353 && NR<=430' ngxtop/ngxtop.py

Let me read the specific print lines for running-for and tables.

RUN grep -n "running for\|records processed\|req/sec\|print_table\|_print\|format\|Summary\|Detailed" ngxtop/ngxtop.py

Let me look at lines around 400-425.

RUN awk 'NR>=400 && NR<=430' ngxtop/ngxtop.py

I now have enough understanding. Let me check config_parser's terminal/option creation and how args map.

RUN grep -n "output\|argparse\|add_argument\|ArgumentParser\|def " ngxtop/config_parser.py

Now let me write PLAN.md. First, I want to confirm how `print` targets stdout and how I can redirect. Let me check the process/report function that prints.

RUN awk 'NR>=355 && NR<=400' ngxtop/ngxtop.py

Let me read the report function and printing.

RUN awk 'NR>=355 && NR<=425' ngxtop/ngxtop.py

Good. Now I understand: `report()` handles status line and tables. Let me read it fully.

RUN grep -n "def report\|def print_\|def process" ngxtop/ngxtop.py

Let me read the process function.

RUN awk 'NR>=260 && NR<=360' ngxtop/ngxtop.py

Now I have full clarity. Let me write the plan.

READ ngxtop/ngxtop.py

I have enough. Let me write the plan now. I'll add `--output-format` to config_parser, and modify ngxtop.py to support json output.

Let me check the exact table-printing function names once more.

RUN grep -n "print_table\|format_table\|def .*table\|def report\|def process\|def main\|def print" ngxtop/ngxtop.py

Now writing PLAN.md.

WRITE PLAN.md
<<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/config_parser.py
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: 配置解析在 config_parser.py 中集中定义 CLI 选项
  依据: ngxtop/config_parser.py:1-20 | import argparse
- 假设: 报表输出由 print_table/report 打印到 stdout，状态行含 "records processed"
  依据: ngxtop/ngxtop.py:1-10 | import sys
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

Now let me read the full ngxtop.py to be precise before editing.

READ ngxtop/ngxtop.py

Let me now write the implementation. First let me re-read config_parser.py fully.

READ ngxtop/config_parser.py

Now let me understand how these options get combined. Let me check the rest of config_parser.

RUN awk 'END{print NR}' ngxtop/config_parser.py

Let me read it fully.

RUN cat -n ngxtop/config_parser.py

Now I need to see the full ngxtop.py to make edits. Let me read it in two parts.

RUN awk 'NR<=290' ngxtop/ngxtop.py

Let me read the rest.

RUN awk 'NR>=290' ngxtop/ngxtop.py

Now I have the full picture. Let me look at print_table function specifically.

RUN grep -n "def print_table\|def report\|def process\|def print_\|def main\|def run" ngxtop/ngxtop.py

Let me read main and print functions.

RUN awk 'NR>=480' ngxtop/ngxtop.py

Let me read the print_table region.

RUN awk 'NR>=440 && NR<=582' ngxtop/ngxtop.py

Now I understand. The key functions:
- `process(args)`: main driving - prints running-for line, then summary/detailed tables
- `print_table`: prints
