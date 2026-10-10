"""ORACLE｜任务 top-n 离线评分器（冻结件 v1.0）

  输入：--repo <工作副本路径>
  输出：JSON —— tests/failed_ecs/outcome（同族契约）
  断言锚：Detailed 基线 4 数据行（|---| 数据行以 / 开头）。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
PY = None
FMT = (
    '$request_time $upstream_response_time $remote_addr - $upstream_addr '
    '[$time_local] $host "$request" $status $bytes_sent "$http_referer" '
    '"$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'
)
TIMEOUT_S = 30


def run_cli(repo: Path, *args: str) -> tuple[int, str, str]:
    r = subprocess.run(
        [str(PY), "-m", "ngxtop.ngxtop", *args],
        cwd=str(repo), capture_output=True, text=True, timeout=TIMEOUT_S,
    )
    return r.returncode, r.stdout, r.stderr


def _strip_running(out: str) -> str:
    return "\n".join(l for l in out.splitlines() if not l.startswith("running for"))


def _detailed_rows(out: str) -> list[str]:
    """Detailed 数据行 = Detailed 段后以 | / 开头的行。"""
    lines = _strip_running(out).splitlines()
    try:
        di = lines.index("Detailed:")
    except ValueError:
        return []
    rows = []
    for l in lines[di + 1:]:
        if l.startswith("| /"):
            rows.append(l)
    return rows


def _summary_present(out: str) -> bool:
    return "Summary:" in out


def t_spec_1(repo) -> tuple[bool, str]:
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                         "--no-follow", "--top", "3")
    rows = _detailed_rows(out)
    base_rows = _detailed_rows((DATA / "baseline-summary.txt").read_text())
    ok = rc == 0 and len(rows) == 3 and rows and rows[0] == base_rows[0]
    return ok, f"rc={rc} rows={len(rows)}"


def t_spec_2(repo) -> tuple[bool, str]:
    baseline = (DATA / "baseline-summary.txt").read_text()
    _, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                        "--no-follow")
    ok = _strip_running(out) == _strip_running(baseline)
    return ok, f"byte-diff={not ok}"


def t_spec_3(repo) -> tuple[bool, str]:
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                         "--no-follow", "--top", "0")
    ok = rc == 0 and len(_detailed_rows(out)) == 0 and _summary_present(out)
    return ok, f"rc={rc} rows={len(_detailed_rows(out))}"


def t_edge_1(repo) -> tuple[bool, str]:
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                         "--no-follow", "--top", "99")
    ok = rc == 0 and len(_detailed_rows(out)) == 4
    return ok, f"rc={rc} rows={len(_detailed_rows(out))}"


def t_edge_2(repo) -> tuple[bool, str]:
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                         "--no-follow", "--top", "2147483647")
    ok = rc == 0 and len(_detailed_rows(out)) == 4
    return ok, f"rc={rc} rows={len(_detailed_rows(out))}"


def t_hidden_1(repo) -> tuple[bool, str]:
    """--top abc：参数层报错（rc!=0 且非 sqlite3 崩溃形态）。"""
    rc, out, err = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                           "--no-follow", "--top", "abc")
    ok = rc != 0 and "sqlite3" not in err and "OperationalError" not in err
    return ok, f"rc={rc} err-type={'sql' if 'sqlite3' in err else 'param'}"


def t_hidden_2(repo) -> tuple[bool, str]:
    """--top -1：参数层报错（rc!=0）。docopt 单破折号解析风险登记：
    --top -1 可能被 docopt 解析为选项缺失参数——两种形态都判 rc!=0。"""
    rc, out, err = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                           "--no-follow", "--top", "-1")
    ok = rc != 0
    return ok, f"rc={rc}"


def t_compat_1(repo) -> tuple[bool, str]:
    """--top 3 -n 10：--top 优先（数据行=3）。"""
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                         "--no-follow", "--top", "3", "-n", "10")
    ok = rc == 0 and len(_detailed_rows(out)) == 3
    return ok, f"rc={rc} rows={len(_detailed_rows(out))}"


TESTS = {
    "T_spec_1": {"fn": t_spec_1, "ec": "RE-1"},
    "T_spec_2": {"fn": t_spec_2, "ec": "RE-2"},
    "T_spec_3": {"fn": t_spec_3, "ec": "RE-3"},
    "T_edge_1": {"fn": t_edge_1, "ec": "EC-1"},
    "T_edge_2": {"fn": t_edge_2, "ec": "EC-2"},
    "T_hidden_1": {"fn": t_hidden_1, "ec": "EC-3"},
    "T_hidden_2": {"fn": t_hidden_2, "ec": "EC-4"},
    "T_compat_1": {"fn": t_compat_1, "ec": "EC-5"},
}


def main():
    global PY
    repo = Path(sys.argv[sys.argv.index("--repo") + 1])
    PY = repo / ".venv/bin/python"
    results, failed_ecs = {}, []
    for tid, spec in TESTS.items():
        try:
            ok, detail = spec["fn"](repo)
            results[tid] = {"pass": ok, "detail": detail}
            if not ok:
                failed_ecs.append(spec["ec"])
        except subprocess.TimeoutExpired:
            results[tid] = {"pass": False, "detail": "TIMEOUT"}
            failed_ecs.append("AUDIT_ERROR:ORACLETIMEOUT")
        except Exception as e:
            results[tid] = {"pass": False, "detail": f"EXCEPTION {e}"}
            failed_ecs.append("AUDIT_ERROR:ORACLEEXCEPTION")
    outcome = "verified" if not failed_ecs else "failed"
    print(json.dumps({"tests": results, "failed_ecs": sorted(set(failed_ecs)),
                      "outcome": outcome}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
