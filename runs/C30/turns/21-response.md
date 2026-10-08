The help text says `log format as specify in log_format directive`, which strongly implies the user should be able to pass the format *name*. Now I have enough understanding to write my plan.

The design:
1. In `config_parser.py`, add `resolve_log_format(name, config_path=None)` that:
   - Looks up the `log_format` named `name` in the nginx config and returns its format string.
   - Returns None if not found.
2. In `ngxtop.py` `process()`, when `--log-format` is not one of the known builtins (combined/common/caddy) and looks like a name, try to resolve it from nginx config; if resolved, use it. If not resolvable, keep existing behavior (treat as literal format string) so nothing regresses.

Let me write the plan.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path" string="true">PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜>
<<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/config_parser.py
- ngxtop/ngxtop.py
- tests/test_named_log_format.py

## ASSUMPTIONS
- 假设: `-f/--log-format` 的取值可能是 nginx `log_format` 指令里定义的格式名（如 `main`），而当前实现只把它当作字面格式串。
  依据: ngxtop/ngxtop.py:11-12 | `    -f <format>, --log-format <format>  log format as specify in log_format directive. [default: combined]`
  验证: 运行 `.venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow`，当前输出 `0 records processed`。
- 假设: 仓库已能把 nginx 配置里命名的 `log_format` 解析为 (name, format) 映射。
  依据: ngxtop/config_parser.py:78-90 | `    log_format = Literal('log_format') + Group(OneOrMore(parameter)) + semicolon`
  验证: `.venv/bin/python -c "from ngxtop import config_parser;print(dict(config_parser.get_log_formats(open('repro/nginx.conf').read())))"` 输出含 `main`。
- 假设: `process()` 里能拿到 `--config` 参数值，可据此定位 nginx 配置文件。
  依据: ngxtop/ngxtop.py:580-588 | `def process(arguments):\n    access_log = arguments['--access-log']\n    log_format = arguments['--log-format']`
  验证: 阅读 process() 函数确认 `arguments['--config']` 可用。

## BEHAVIOR_DELTAS
- 增量: 当 `-f <name>` 的值命中 nginx 配置中定义的 `log_format` 名时，解析为对应的格式串，从而正确解析 repro/access.log 的 5 行记录。
  VERIFY: `.venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow -c repro/nginx.conf 2>/dev/null | grep -E "5 records processed"`
- 增量: 当 `-f` 值为内置格式（combined/common/caddy）或无法在配置中解析时，保持原有字面格式串行为不变。
  VERIFY: `.venv/bin/python -m pytest tests/test_characterization.py -q`

## NON_GOALS
- 非目标: 不修改默认配置探测（无 -f/-c 时的自动探测）行为。
  GUARD: `.venv/bin/python -m pytest tests/test_config_parser.py -q`
- 非目标: 不改动 Caddy JSON 格式解析逻辑。
  GUARD: `.venv/bin/python -m pytest tests/test_caddy_integration.py tests/test_json_extraction_fix.py -q`

## TEST_PLAN
1. 新增 tests/test_named_log_format.py，覆盖：命名格式解析成功、多行 conf、未知名字回退字面串。
2. 运行 `.venv/bin/python -m pytest tests/ -q` 全绿。
3. 手工运行 CLI 复现命令确认有结果行。
FILE_CONTENTS
</｜｜DSML｜｜ calls>
