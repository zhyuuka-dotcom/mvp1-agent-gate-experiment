# PLAN

## TOUCH_SET
- src_app.py
- src_util.py

## ASSUMPTIONS
- 假设: 超时默认值为 30 秒
  依据: src_app.py:2-2 | DEFAULT_TIMEOUT = 30
  验证: 读文件确认
- 假设: 工具模块有 helper
  依据: src_util.py:4-4 | def helper(): pass
  验证: grep helper

## BEHAVIOR_DELTAS
- 增量: 增加输出格式分支
  VERIFY: .venv/bin/python -m pytest tests/ -q

## NON_GOALS
- 非目标: 不改动无关模块
  GUARD: tests/test_smoke.py

## TEST_PLAN
先跑存量，再跑新功能用例
