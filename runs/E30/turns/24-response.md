My WRITE got truncated/misrouted again. The harness is having serious tool-routing problems. Let me try a clean, complete WRITE for PLAN.md.

WRITE PLAN.md
<<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/config_parser.py
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: get_log_formats 能从 nginx 配置文本中解析出具名 log_format 定义的格式串，该格式串可直接用于构建解析模式。
  依据: ngxtop/config_parser.py:74-83 | def get_log_formats(config):
    """
    Parse config for log_format directives
    :return: iterator over ('format name', 'format string') tuple of found directives
    """
    # log_format name [params]
    log_format = Literal('log_format') + parameter + Group(OneOrMore(parameter)) + semicolon
    log_format.ignore(pythonStyleComment)

    for directive in log_format.searchString(config).asList():
        name = directive[1]
        format_string = ''.join(directive[2])
        yield name, format_string
  验证: 运行 `.venv/bin/python -c "from ngxtop import config_parser; print(dict(config_parser.get_log_formats(open('repro/nginx_multiline.conf').read())))"` 应输出含 main 与其格式串。
- 假设: 当同时给出 -l 与具名 -f 时，process() 不会解析配置文件，因此 build_pattern 把名称当作字面格式串，导致无法匹配日志行。
  依据: ngxtop/config_parser.py:118-132 | def build_pattern(log_format):
    """
    Build regular expression to parse given format.
    :param log_format: format string to parse
    :return: regular expression to parse given format
    """
    if log_format == 'combined':
        log_format = LOG_FORMAT_COMBINED
    elif log_format == 'common':
        log_format = LOG_FORMAT_COMMON
    elif log_format == 'caddy':
        return 'caddy'  # Special case for Caddy JSON format
    pattern = re.sub(REGEX_SPECIAL_CHARS, r'\\\1', log_format)
    pattern = re.sub(REGEX_LOG_FORMAT_VARIABLE, '(?P<\\1>.*)', pattern)
    return re.compile(pattern)
  验证: 运行 `.venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow`，当前输出 0 records processed。

## BEHAVIOR_DELTAS
- 增量: 当 -f 传入的名称不是 built-in（combined/common/caddy）时，ngxtop 会尝试从 nginx 配置文件中解析该名称对应的格式串（无 --config 时自动探测），并据此构建解析模式，从而正确解析日志行。
  VERIFY: `.venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow -c repro/nginx_multiline.conf` 输出含 `5 records processed`。

## NON_GOALS
- 非目标: 不改变默认 combined/common/caddy 格式的行为，也不改变既有配置探测流程的输出。
  GUARD: `.venv/bin/python -m pytest tests/test_characterization.py -q`

## TEST_PLAN
1. 运行 `.venv/bin/python -m pytest tests/ -q` 确认基线。
2. 在 config_parser.py 增加按名称解析格式串的辅助函数。
3. 在 ngxtop.py 的 process() 中，当 -f 为具名格式且能解析到配置时替换为真实格式串。
4. 用复现材料手动验证 -f main 场景。
5. 重跑全量测试。
FILE_CONTENTS
