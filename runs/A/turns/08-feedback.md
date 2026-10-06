READ 错误: 文件不存在: .
"""特征化测试：固化文档记载的既有公开行为（MVP-1 冻结件）。

每条断言的规格出处见各测试的 provenance 注释。
这些测试在 T1 任务开始前即为绿；任何实现修改不得使其变红。
"""
import os
import subprocess
from pathlib import Path

REPO = Path(os.environ.get("MVP1_REPO", Path(__file__).resolve().parent.parent))
PY = REPO / ".venv/bin/python"
FIX = REPO / "repro"


def run_cli(*args):
    return subprocess.run(
        [str(PY), "-m", "ngxtop.ngxtop", *args],
        capture_output=True, text=True, cwd=str(REPO), timeout=60,
    )


def test_default_combined_top():
    # provenance: docopt usage（ngxtop.py 顶部 Usage 块）默认格式 combined；
    # README §Usage 基本用法 `$ ngxtop`。
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow")
    assert r.returncode == 0
    assert "2 records processed" in r.stdout
    assert "Summary:" in r.stdout


def test_group_by_single_column():
    # provenance: README/docopt 示例 `$ ngxtop --group-by remote_addr`。
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow", "-g", "remote_addr")
    assert r.returncode == 0
    assert "remote_addr" in r.stdout
    assert "10.0.0.1" in r.stdout


def test_order_by_count():
    # provenance: docopt usage `-o, --order-by` 选项。
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow", "-o", "count")
    assert r.returncode == 0
    assert "Summary:" in r.stdout
