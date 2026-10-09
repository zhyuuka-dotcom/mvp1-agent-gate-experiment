Now I'll add a test file for median behavior.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">tests/test_median_bytes_sent.py</｜｜DSML｜｜ parameter>
<<<FILE_CONTENTS
"""Tests for the median of bytes_sent in the default report.

Feature request: add median of bytes_sent to the report so the typical
request size can be seen next to the average.
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


def test_median_aggregate_odd_count():
    from ngxtop.ngxtop import Median
    agg = Median()
    for v in [5120, 153, 2048, 512, 300]:
        agg.step(v)
    assert agg.finalize() == 512


def test_median_aggregate_even_count():
    from ngxtop.ngxtop import Median
    agg = Median()
    for v in [153, 5120]:
        agg.step(v)
    assert agg.finalize() == (153 + 5120) / 2.0


def test_median_aggregate_empty():
    from ngxtop.ngxtop import Median
    assert Median().finalize() is None


def test_median_aggregate_ignores_none():
    from ngxtop.ngxtop import Median
    agg = Median()
    for v in [None, 10, None, 20, 30]:
        agg.step(v)
    assert agg.finalize() == 20


def test_report_has_median_column():
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow")
    assert r.returncode == 0
    assert "median_bytes_sent" in r.stdout
    # median of [5120, 153] is 2636.5, as is the average for two values
    assert "2636.500" in r.stdout
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
