Combined format works: 2 records, even count → (5120+153)/2 = 2636.5. Now write the new test file, then update README.

tests/test_median.py — verify median values via CLI and via the Median class directly.

WRITE tests/test_median.py
<<<FILE_CONTENTS
"""Tests for the median(bytes_sent) statistic added to the default report.

The feature request asks the default report to show the median of bytes_sent
next to its average. These tests pin the new ``median_bytes_sent`` column in
both the Summary and Detailed tables and check the numeric value.
"""
import os
import re
import subprocess
from pathlib import Path

REPO = Path(os.environ.get("MVP1_REPO", Path(__file__).resolve().parent.parent))
PY = REPO / ".venv/bin/python"
FIX = REPO / "repro"


def _main_format():
    text = (FIX / "nginx.conf").read_text()
    return re.search(r"log_format\s+main\s+'(.*?)';", text).group(1)


def run_cli(*args):
    return subprocess.run(
        [str(PY), "-m", "ngxtop.ngxtop", *args],
        capture_output=True, text=True, cwd=str(REPO), timeout=60,
    )


def test_summary_has_median_column():
    r = run_cli("-l", str(FIX / "access.log"), "-f", _main_format(), "--no-follow")
    assert r.returncode == 0
    assert "median_bytes_sent" in r.stdout
    assert "Summary:" in r.stdout
    assert "Detailed:" in r.stdout


def test_summary_median_value_odd_count():
    # bytes_sent = 5120, 153, 2048, 512, 300 -> sorted middle value is 512.
    r = run_cli("-l", str(FIX / "access.log"), "-f", _main_format(), "--no-follow")
    summary = r.stdout.split("Summary:")[1].split("Detailed:")[0]
    assert "512.000" in summary


def test_median_aggregate_even_and_odd():
    from ngxtop.ngxtop import Median

    m = Median()
    for v in [10, 2, 8, 4]:
        m.step(v)
    assert m.finalize() == 5.0  # (4 + 2) / 2? sorted [2,4,8,10] -> (4+8)/2 = 6.0

    m2 = Median()
    for v in [5, 1, 3]:
        m2.step(v)
    assert m2.finalize() == 3.0


def test_median_ignores_none_and_empty():
    from ngxtop.ngxtop import Median

    m = Median()
    m.step(None)
    m.step(7)
    m.step(None)
    assert m.finalize() == 7.0

    empty = Median()
    assert empty.finalize() is None


def test_combined_default_report_has_median():
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow")
    assert r.returncode == 0
    assert "median_bytes_sent" in r.stdout
FILE_CONTENTS

Wait, test_median_aggregate_even_and_odd has a wrong assertion: sorted [2,4,8,10] → mid=2, (values[1]+values[2])/2 = (4+8)/2 = 6.0. I wrote 5.0 then a comment. Fix to 6.0.

Let me rewrite that test correctly.

WRITE tests/test_median.py
<<<FILE_CONTENTS
"""Tests for the median(bytes_sent) statistic added to the default report.

The feature request asks the default report to show the median of bytes_sent
next to its average. These tests pin the new ``median_bytes_sent`` column in
both the Summary and Detailed tables and check the numeric value.
"""
import os
import re
import subprocess
from pathlib import Path

REPO = Path(os.environ.get("MVP1_REPO", Path(__file__).resolve().parent.parent))
PY = REPO / ".venv/bin/python"
FIX = REPO / "repro"


def _main_format():
    text = (FIX / "nginx.conf").read_text()
    return re.search(r"log_format\s+main\s+'(.*?)';", text).group(1)


def run_cli(*args):
    return subprocess.run(
        [str(PY), "-m", "ngxtop.ngxtop", *args],
        capture_output=True, text=True, cwd=str(REPO), timeout=60,
    )


def test_summary_has_median_column():
    r = run_cli("-l", str(FIX / "access.log"), "-f", _main_format(), "--no-follow")
    assert r.returncode == 0
    assert "median_bytes_sent" in r.stdout
    assert "Summary:" in r.stdout
    assert "Detailed:" in r.stdout


def test_summary_median_value_odd_count():
    # bytes_sent = 5120, 153, 2048, 512, 300 -> sorted middle value is 512.
    r = run_cli("-l", str(FIX / "access.log"), "-f", _main_format(), "--no-follow")
    summary = r.stdout.split("Summary:")[1].split("Detailed:")[0]
    assert "512.000" in summary


def test_median_aggregate_even_and_odd():
    from ngxtop.ngxtop import Median

    even = Median()
    for v in [10, 2, 8, 4]:  # sorted [2, 4, 8, 10]
        even.step(v)
    assert even.finalize() == 6.0

    odd = Median()
    for v in [5, 1, 3]:  # sorted [1, 3, 5]
        odd.step(v)
    assert odd.finalize() == 3.0


def test_median_ignores_none_and_empty():
    from ngxtop.ngxtop import Median

    m = Median()
    m.step(None)
    m.step(7)
    m.step(None)
    assert m.finalize() == 7.0

    empty = Median()
    assert empty.finalize() is None


def test_combined_default_report_has_median():
    r = run_cli("-l", str(FIX / "combined.log"), "--no-follow")
    assert r.returncode == 0
    assert "median_bytes_sent" in r.stdout
FILE_CONTENTS

Send.
