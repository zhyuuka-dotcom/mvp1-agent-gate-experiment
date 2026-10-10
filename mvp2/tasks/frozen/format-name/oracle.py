"""ORACLE｜任务 format-name 离线评分器（冻结件 v1.0）

  输入：--repo <工作副本路径>
  输出：JSON —— tests/failed_ecs/outcome（同 csv-export oracle 契约）
  冻结断言集与 EC 映射见 COVERAGE.md。
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


def _summary_numbers(out: str) -> list[str]:
    pipe_rows = re.findall(r"^\|.*\|$", out, re.M)
    if len(pipe_rows) < 3:
        return []
    return [c.strip() for c in pipe_rows[2].strip().strip("|").split("|")]


def t_spec_1(repo) -> tuple[bool, str]:
    """-f main（base.conf）数值 == -f <格式串>（名字解析正确）。"""
    rc_a, out_a, _ = run_cli(repo, "-l", str(DATA / "access.log"),
                             "-c", str(DATA / "base.conf"), "-f", "main", "--no-follow")
    rc_b, out_b, _ = run_cli(repo, "-l", str(DATA / "access.log"),
                             "-f", FMT, "--no-follow")
    if rc_a != 0:
        return False, f"name-rc={rc_a}"
    return _summary_numbers(out_a) == _summary_numbers(out_b), \
        f"name={_summary_numbers(out_a)} direct={_summary_numbers(out_b)}"


def t_spec_2(repo) -> tuple[bool, str]:
    """格式串直传零回归（基线快照，剥动态行）。"""
    baseline = (DATA / "baseline-summary.txt").read_text()
    _, out, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT, "--no-follow")
    return (_strip_running(out) == _strip_running(baseline)), "byte-diff"


def t_spec_3(repo) -> tuple[bool, str]:
    """未知名：stderr 含 unknown format name 且 rc!=0。"""
    rc, _, err = run_cli(repo, "-l", str(DATA / "access.log"),
                         "-c", str(DATA / "base.conf"), "-f", "nosuchname", "--no-follow")
    ok = rc != 0 and "unknown format name" in err
    return ok, f"rc={rc} err={'yes' if 'unknown format name' in err else 'no'}"


def t_edge_1(repo) -> tuple[bool, str]:
    """dup.conf 两个同名 main → 取首个（bytes_sent 定义，非 request_length）。"""
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"),
                         "-c", str(DATA / "dup.conf"), "-f", "main", "--no-follow")
    if rc != 0:
        return False, f"rc={rc}"
    # 首个定义 = 标准 bytes_sent → avg 与基线一致 1626.600；
    # 若取第二个（request_length）数值必然不同
    got = _summary_numbers(out)
    rc_b, out_b, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT, "--no-follow")
    want = _summary_numbers(out_b)
    return got == want, f"got={got} want-first={want}"


def t_edge_2(repo) -> tuple[bool, str]:
    """带引号名 'my format' 可解析（数值==直接串）。"""
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"),
                         "-c", str(DATA / "quoted.conf"), "-f", "my format", "--no-follow")
    if rc != 0:
        return False, f"rc={rc}"
    got = _summary_numbers(out)
    rc_b, out_b, _ = run_cli(repo, "-l", str(DATA / "access.log"), "-f", FMT, "--no-follow")
    return got == _summary_numbers(out_b), f"got={got}"


def t_compat_1(repo) -> tuple[bool, str]:
    """名解析 × --no-follow × -l 组合（值等价 T_spec_1 并 rc=0）。"""
    rc, out, _ = run_cli(repo, "-l", str(DATA / "access.log"),
                         "-c", str(DATA / "base.conf"), "-f", "main", "--no-follow")
    ok = rc == 0 and bool(_summary_numbers(out))
    return ok, f"rc={rc}"


def t_hidden_1(repo) -> tuple[bool, str]:
    """大小写敏感：-f Main 报错（unknown format name）。"""
    rc, _, err = run_cli(repo, "-l", str(DATA / "access.log"),
                         "-c", str(DATA / "base.conf"), "-f", "Main", "--no-follow")
    ok = rc != 0 and "unknown format name" in err
    return ok, f"rc={rc}"


TESTS = {
    "T_spec_1": {"fn": t_spec_1, "ec": "RE-1"},
    "T_spec_2": {"fn": t_spec_2, "ec": "RE-2"},
    "T_spec_3": {"fn": t_spec_3, "ec": "RE-3"},
    "T_edge_1": {"fn": t_edge_1, "ec": "EC-1"},
    "T_edge_2": {"fn": t_edge_2, "ec": "EC-2"},
    "T_compat_1": {"fn": t_compat_1, "ec": "EC-3"},
    "T_hidden_1": {"fn": t_hidden_1, "ec": "EC-4"},
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
