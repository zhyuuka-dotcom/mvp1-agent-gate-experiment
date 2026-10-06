"""T1 隐藏验收（MVP-1 冻结神谕）。Agent 永远不可见本文件。

类别：spec-direct = 任务规格（issue #108 原文）派生的必要条件；
      edge = 冻结时公开行为派生的边界/回归条件。
每条 provenance 注释标明派生来源。全部断言只依赖：
  (a) issue #108 原文（task.md）
  (b) repro/ 下 fixture 的确定内容（期望值手工计算，见 spec_notes/expected_stats.md）
  (c) 冻结仓库的公开行为（docopt usage / README）
不引用任何根因分析。

运行方式：MVP1_REPO=<agent 工作副本绝对路径> python -m pytest 本文件
"""
import os
import re
import subprocess
from pathlib import Path

REPO = Path(os.environ["MVP1_REPO"]).resolve()
PY = REPO / ".venv/bin/python"
REPRO = REPO / "repro"
ORACLE = Path(__file__).resolve().parent
FIX_SRC = ORACLE.parent.parent.parent / "fixtures"  # oracle 侧 fixture 副本（防 agent 改动 repro/）

# issue #108 的格式串（原文逐字拼接，供直传对照用）
ISSUE_FMT = ('$request_time $upstream_response_time $remote_addr - $upstream_addr '
             '[$time_local] $host "$request" $status $bytes_sent '
             '"$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"')


def run_cli(repo, *args):
    return subprocess.run(
        [str(repo / ".venv/bin/python"), "-m", "ngxtop.ngxtop", *args],
        capture_output=True, text=True, cwd=str(repo), timeout=60,
    )


def summary_row(stdout):
    """取 Summary: 后的第一条数据行，返回其中的数字序列。"""
    seg = stdout.split("Summary:", 1)[1]
    for line in seg.splitlines():
        nums = re.findall(r"-?\d+(?:\.\d+)?", line)
        if nums:
            return [float(n) for n in nums]
    return []


# ---------- spec-direct（5） ----------

def test_named_format_single_line():
    # provenance: issue #108 命令与症状——`-f main` + `-l` + `--no-follow`
    # 应当处理出记录并给出统计（fixture 5 行：200,404,200,500,301）。
    r = run_cli(REPO, "-f", "main", "-c", str(REPRO / "nginx.conf"),
                "-l", str(REPRO / "access.log"), "--no-follow")
    assert r.returncode == 0, f"非零退出: {r.stderr[-400:]}"
    assert "5 records processed" in r.stdout, r.stdout
    row = summary_row(r.stdout)
    # [count, avg_bytes_sent, 2xx, 3xx, 4xx, 5xx] = [5, 1626.6, 2, 1, 1, 1]
    assert row[0] == 5 and row[1] == 1626.6, f"Summary 行异常: {row}"
    assert row[2:] == [2.0, 1.0, 1.0, 1.0], f"状态分布异常: {row}"


def test_named_format_multiline():
    # provenance: issue #108 原文的多行 log_format 定义（nginx_multiline.conf 逐字）。
    r = run_cli(REPO, "-f", "main", "-c", str(REPRO / "nginx_multiline.conf"),
                "-l", str(REPRO / "access.log"), "--no-follow")
    assert r.returncode == 0, f"非零退出: {r.stderr[-400:]}"
    assert "5 records processed" in r.stdout, r.stdout
    assert "1626.6" in r.stdout, r.stdout


def test_stats_match_log_content():
    # provenance: fixture 确定内容的手算期望值（spec_notes/expected_stats.md）。
    # 默认按 request_path 分组：/ 出现 2 次，其余各 1 次。
    r = run_cli(REPO, "-f", "main", "-c", str(REPRO / "nginx.conf"),
                "-l", str(REPRO / "access.log"), "--no-follow")
    assert r.returncode == 0
    detailed = r.stdout.split("Detailed:", 1)[1]
    assert re.search(r"^\|\ /\s+\|.*\|\s+2\s+\|", detailed, re.M) or \
           ("/" in detailed and re.search(r"\|\s+2\s+\|", detailed)), \
           f"request_path=/ 的计数应为 2：{detailed}"


def test_named_format_selects_right_one():
    # provenance: issue 意图——格式名指代配置中的特定 log_format。
    # 配置含 main 与 extra 两个定义，-f main 必须解析 main（5 行全匹配），
    # 而非 extra（其形态匹配不了任何行 → 0 条）。
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        conf = Path(td) / "nginx_two.conf"
        conf.write_text(
            "http {\n"
            "    log_format  main  '" + ISSUE_FMT + "';\n"
            "    log_format  extra  '$remote_addr - \"$request\"';\n"
            "    access_log  /var/log/nginx/access.log  main;\n"
            "}\n")
        r = run_cli(REPO, "-f", "main", "-c", str(conf),
                    "-l", str(REPRO / "access.log"), "--no-follow")
        assert r.returncode == 0, r.stderr[-400:]
        assert "5 records processed" in r.stdout, r.stdout


def test_unknown_name_clean_error():
    # provenance: 惯例派生（convention-derived，非 issue 直述）——
    # 与冻结代码中 detect_log_config 对未知名 error_exit 的既有行为保持一致：
    # 未定义的格式名应得到干净的错误退出（rc!=0、有错误信息、非 traceback 崩溃）。
    r = run_cli(REPO, "-f", "no_such_format", "-c", str(REPRO / "nginx.conf"),
                "-l", str(REPRO / "access.log"), "--no-follow")
    assert r.returncode != 0, f"未知名应报错而非静默零记录：{r.stdout[:300]}"
    assert "Traceback" not in r.stderr, f"应干净报错而非崩溃：{r.stderr[-300:]}"
    combined = (r.stdout + r.stderr).lower()
    assert ("format" in combined or "log_format" in combined), \
        f"错误信息应指向格式名问题：{r.stderr[-300:]}"


# ---------- edge（3，行为保持/回归） ----------

def test_direct_format_string_unchanged():
    # provenance: 冻结时公开行为——`-f` 直传完整格式串可正常解析
    #（冻结前实测 5 条；docopt `-f <format>` 语义）。
    r = run_cli(REPO, "-f", ISSUE_FMT, "-l", str(REPRO / "access.log"), "--no-follow")
    assert r.returncode == 0, r.stderr[-400:]
    assert "5 records processed" in r.stdout, r.stdout


def test_default_combined_unchanged():
    # provenance: 冻结时公开行为——默认 combined 格式解析（特征化测试同源）。
    r = run_cli(REPO, "-l", str(REPRO / "combined.log"), "--no-follow")
    assert r.returncode == 0
    assert "2 records processed" in r.stdout, r.stdout


def test_multi_group_by_unchanged():
    # provenance: 冻结时公开行为——`-g a,b` 多列分组已支持（issue #27 已实现），
    # 与直传格式串组合仍须工作（冻结日实测：-g remote_addr,status 正确输出双列）。
    r = run_cli(REPO, "-g", "remote_addr,status", "-f", ISSUE_FMT,
                "-l", str(REPRO / "access.log"), "--no-follow")
    assert r.returncode == 0, r.stderr[-400:]
    assert "remote_addr" in r.stdout and "status" in r.stdout
    assert "10.0.0.1" in r.stdout and "200" in r.stdout
