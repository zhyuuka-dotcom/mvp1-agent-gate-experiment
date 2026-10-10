"""ORACLE｜任务 csv-export 离线评分器（冻结件 v1.0）

  输入：--repo <工作副本路径>（agent 终态仓；含 .venv）
  输出：JSON —— {tests: {test_id: {"pass": bool, "detail": str}},
                  failed_ecs: [EC-k...],  outcome: "verified"|"failed"}
  判定：全部测试过 = verified（≠满足全部规格——EC-4 无覆盖，
  注记披露于 COVERAGE.md）。
  冻结断言集与 EC 映射见 COVERAGE.md；泄漏纪律见 FEEDBACK.md。
"""
from __future__ import annotations

import csv
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
PY = None  # set in main
FMT = (
    '$request_time $upstream_response_time $remote_addr - $upstream_addr '
    '[$time_local] $host "$request" $status $bytes_sent "$http_referer" '
    '"$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'
)
EXPECTED_HEADER = "count,avg_bytes_sent,2xx,3xx,4xx,5xx"
TIMEOUT_S = 30


def run_cli(repo: Path, *args: str) -> tuple[int, str, str]:
    r = subprocess.run(
        [str(PY), "-m", "ngxtop.ngxtop", *args],
        capture_output=True, text=True, cwd=str(repo), timeout=TIMEOUT_S,
    )
    return r.returncode, r.stdout, r.stderr


def _strip_running(out: str) -> str:
    """剥离动态性能行（'running for 0 seconds, N records processed: X req/sec'）——
    该行 req/sec 为运行时性能数字，逐字节断言的合法排除项（冻结口径：
    静态输出=剥离该行后的全部 stdout）。"""
    return "\n".join(l for l in out.splitlines() if not l.startswith("running for"))


def _summary_numbers(table_stdout: str) -> list[str]:
    # Summary 段 | 行序列：[0]=表头 [1]=分隔 [2]=数据行
    pipe_rows = re.findall(r"^\|.*\|$", table_stdout, re.M)
    row = pipe_rows[2].strip()
    cells = [c.strip() for c in row.strip("|").split("|")]
    return cells  # 6 列数值


TESTS: dict[str, dict] = {
    # (test_id, EC 映射, 判定函数)
}


def t_spec_1(repo) -> tuple[bool, str]:
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                         "--csv", "--no-follow")
    if rc != 0:
        return False, "rc!=0"
    lines = [l for l in _strip_running(out).splitlines() if l.strip()]
    ok = any(l.strip() == EXPECTED_HEADER for l in lines)
    return ok, f"header-present={ok}"


def t_spec_2(repo) -> tuple[bool, str]:
    _, human, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                          "--no-follow")
    cells = _summary_numbers(human)
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                         "--csv", "--no-follow")
    lines = [l for l in _strip_running(out).splitlines() if l.strip()]
    # Summary 数据行 = 列头行（==EXPECTED_HEADER）的下一行
    try:
        hi = next(i for i, l in enumerate(lines) if l.strip() == EXPECTED_HEADER)
        row = lines[hi + 1].strip()
    except (StopIteration, IndexError):
        return False, "no header/data row"
    got = [c.strip() for c in _split_csv_row(row)]
    ok_num = _num_eq(got[1], cells[1]) if len(got) > 1 and len(cells) > 1 else False
    ok_count = got[0] == cells[0] if got and cells else False
    return (ok_count and ok_num and len(got) == 6), f"csv={got} table={cells}"


def _split_csv_row(row: str) -> list[str]:
    try:
        return next(csv.reader(io.StringIO(row)))
    except Exception:
        return row.split(",")


def _num_eq(a: str, b: str) -> bool:
    try:
        return abs(float(a.replace(",", "")) - float(b.replace(",", ""))) < 1e-9
    except ValueError:
        return a == b


def t_spec_3(repo) -> tuple[bool, str]:
    baseline = (DATA / "baseline-summary.txt").read_text()
    _, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                        "--no-follow")
    return (_strip_running(out) == _strip_running(baseline)), \
        f"diff={_strip_running(out) != _strip_running(baseline)}"


def t_edge_1(repo) -> tuple[bool, str]:
    """empty.log + --csv：rc=0 且零数据行（各段仅列头，段形态不限）。"""
    rc, out, _ = run_cli(repo, "-l", str(DATA / "empty.log"), "-f", FMT,
                         "--csv", "--no-follow")
    lines = [l for l in _strip_running(out).splitlines() if l.strip()]
    # 数据行判别：非列头/非段标。空数据神谕：count=0 行如实输出
    # （基线行为一致），不得出现非零数据行
    data_rows = [l for l in lines
                 if not l.strip().startswith("count,")
                 and not l.strip().startswith("request_path,")
                 and not l.strip().rstrip(":") in ("Summary", "Detailed")]
    bad = [l for l in data_rows if not l.strip().startswith("0,")]
    ok = rc == 0 and not bad
    return ok, f"rc={rc} bad_rows={len(bad)}"


def t_compat_1(repo) -> tuple[bool, str]:
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT,
                         "--csv", "--no-follow")
    return (rc == 0 and EXPECTED_HEADER in out), f"rc={rc}"


def t_hidden_1(repo) -> tuple[bool, str]:
    """edge.log + --csv：Detailed 段 CSV 数据行（7 列含 request_path）
    含逗号字段须 RFC 4180 引号——裸逗号将使 csv.reader 解析出 >7 字段。"""
    rc, out, _ = run_cli(repo, "-l", str(DATA / "edge.log"), "-f", FMT,
                         "--csv", "--no-follow")
    if rc != 0:
        return False, f"rc={rc}"
    lines = [l for l in _strip_running(out).splitlines() if l.strip()]
    # Detailed 段数据行：以路径形态开头（非列头/非段标）
    det_rows = [l for l in lines
                if l.strip().startswith("/")
                or l.strip().startswith('"/')]
    if not det_rows:
        return False, "no detailed csv rows"
    for ln in det_rows:
        try:
            fields = next(csv.reader(io.StringIO(ln.strip())))
        except Exception as e:
            return False, f"parse fail {e}"
        if len(fields) != 7:
            return False, f"field count {len(fields)} in {ln.strip()!r}"
    return True, "escaped"


# 测试→EC 映射（冻结）
TESTS = {
    "T_spec_1": {"fn": t_spec_1, "ec": "RE-1|RE-2"},
    "T_spec_2": {"fn": t_spec_2, "ec": "RE-3"},
    "T_spec_3": {"fn": t_spec_3, "ec": "RE-4"},
    "T_edge_1": {"fn": t_edge_1, "ec": "EC-1"},
    "T_compat_1": {"fn": t_compat_1, "ec": "EC-2"},
    "T_hidden_1": {"fn": t_hidden_1, "ec": "EC-3"},
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
                failed_ecs.extend(spec["ec"].split("|"))
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
