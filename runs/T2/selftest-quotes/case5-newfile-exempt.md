# PLAN

## TOUCH_SET
- src_app.py
- tests/test_new_feature.py

## ASSUMPTIONS
- 假设: 超时默认值为 30 秒
  依据: src_app.py:2-2 | DEFAULT_TIMEOUT = 30
  验证: 读文件确认
- 假设: 冒烟测试存在
  依据: tests/test_smoke.py:1-2 | def test_smoke():
  验证: 跑一次

## BEHAVIOR_DELTAS
- 增量: 增加输出格式分支
  VERIFY: .venv/bin/python -m pytest tests/ -q

## NON_GOALS
- 非目标: 不改动无关模块
  GUARD: tests/test_smoke.py

## TEST_PLAN
先跑存量，再跑新功能用例
