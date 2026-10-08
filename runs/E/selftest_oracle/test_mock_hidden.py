"""INDEPENDENT_ACCEPTANCE 自测用 mock 神谕（harness 侧基建，永不给 agent）。

2 spec + 1 edge；test_mock_spec_mark 以工作副本内 MARK 文件存在与否定绿红，
用于构造 PASS/FAIL 两种验收路径；test_mock_extra_fail 用 REPO 断言构造
第三种红（存量套件之外的独立红点）。运行方式与真神谕一致：
MVP1_REPO=<repo> pytest 本文件
"""
import os
from pathlib import Path

REPO = Path(os.environ["MVP1_REPO"]).resolve()


def test_mock_spec_always():
    assert True


def test_mock_spec_mark():
    assert (REPO / "MARK").exists(), "MARK 缺席——构造的 spec 红点"


def test_mock_edge_always():
    assert REPO.is_dir()
