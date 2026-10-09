import pathlib
def plan(touch, assums, name):
    body = ["# PLAN", "", "## TOUCH_SET"]
    body += [f"- {t}" for t in touch]
    body += ["", "## ASSUMPTIONS"]
    body += assums
    body += ["", "## BEHAVIOR_DELTAS", "- 增量: 增加输出格式分支", "  VERIFY: .venv/bin/python -m pytest tests/ -q", ""]
    body += ["## NON_GOALS", "- 非目标: 不改动无关模块", "  GUARD: tests/test_smoke.py", ""]
    body += ["## TEST_PLAN", "先跑存量，再跑新功能用例"]
    pathlib.Path(name).write_text("\n".join(body) + "\n")

A1 = '- 假设: 超时默认值为 30 秒\n  依据: src_app.py:2-2 | DEFAULT_TIMEOUT = 30\n  验证: 读文件确认'
A2 = '- 假设: 冒烟测试存在\n  依据: tests/test_smoke.py:1-2 | def test_smoke():\n  验证: 跑一次'
A3 = '- 假设: 工具模块有 helper\n  依据: src_util.py:4-4 | def helper(): pass\n  验证: grep helper'
A_long = '- 假设: 长行存在\n  依据: src_util.py:2-2 | LONG_MARKER_' + 'x'*130 + '_END\n  验证: wc -L'
A_fake = '- 假设: 虚构行存在\n  依据: src_app.py:2-2 | TIMEOUT_IS_FORTY_TWO = 42\n  验证: 不存在则拒'
A_multi = '- 假设: 引用了两行\n  依据: src_app.py:2-4 | """Sample app module."""\nDEFAULT_TIMEOUT = 30\n  验证: 多行不是单行'

# case1：双既有文件各一条有效单行引文 → 期望过
plan(["src_app.py", "src_util.py"], [A1, A3], "case1-valid.md")
# case2：src_app 的引文为虚构行 → 期望拒（仅 src_app 缺有效引文）
plan(["src_app.py", "tests/test_smoke.py"], [A_fake, A2], "case2-nonexistent-line.md")
# case3：src_util 的引文为真实 148 字符行（超 120） → 期望拒
plan(["src_util.py", "tests/test_smoke.py"], [A_long, A2], "case3-too-long.md")
# case4：src_app 的引文跨两行（多行文本） → 期望拒
plan(["src_app.py", "tests/test_smoke.py"], [A_multi, A2], "case4-multiline.md")
# case5：TOUCH_SET 含新建文件（父目录存在）且既有文件有有效引文 → 期望过（新建豁免）
plan(["src_app.py", "tests/test_new_feature.py"], [A1, A2], "case5-newfile-exempt.md")
print("5 plans written (v2)")
