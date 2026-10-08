"""T3 隐藏验收（MVP-1 冻结神谕）。Agent 永远不可见本文件。

类别：spec-direct = 任务规格（功能请求原文 + 仓库公开惯例）派生的必要条件；
      edge = 冻结时公开行为派生的边界/回归条件。
每条 provenance 注明派生来源。全部断言只依赖：
  (a) 功能请求原文（task.md：中位数与 bytes_sent、与平均值并见）
  (b) 仓库公开惯例（DEFAULT_QUERIES 的列命名/列序/双表结构与
      `avg(bytes_sent) AS avg_bytes_sent` 既有形态）
  (c) oracle 侧 fixture 副本的确定内容（期望值手工计算，
      见 spec_notes/expected_stats.md）
断言不引用任何封存分析文件。

运行方式：MVP1_REPO=<agent 工作副本绝对路径> python -m pytest 本文件
（fixture 用 oracle 侧副本路径调用 agent 的 CLI——内容与冻结 repro 逐字节
一致；agent 改动其工作副本内 repro/ 不影响神谕判定）
"""
import os
import subprocess
from pathlib import Path

REPO = Path(os.environ["MVP1_REPO"]).resolve()
PY = REPO / ".venv/bin/python"
ORACLE = Path(__file__).resolve().parent.parent  # tasks/T3/oracle/
FIX = ORACLE / "fixtures"  # oracle 侧 fixture 副本（防 agent 改动 repro/）

# issue 格式串（repro/nginx.conf log_format main 内容逐字，供直传调用用）
FMT_MAIN = ('$request_time $upstream_response_time $remote_addr - $upstream_addr '
            '[$time_local] $host "$request" $status $bytes_sent '
            '"$http_referer" "$http_user_agent" "$gzip_ratio" '
            '"$http_x_forwarded_for" - "$server_addr"')


def run_cli(*args):
    cmd = [str(PY), "-m", "ngxtop.ngxtop"] + [str(a) for a in args]
    return subprocess.run(cmd, cwd=str(REPO), capture_output=True,
                          text=True, timeout=120)


def parse_tables(stdout):
    """把 orgtbl 输出解析为 {节名: {"headers": [...], "rows": [[...], ...]}}。"""
    tables, current = {}, None
    for line in stdout.splitlines():
        s = line.strip()
        if s in ("Summary:", "Detailed:"):
            current = s[:-1]
            tables[current] = {"headers": None, "rows": []}
            continue
        if current is None or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if set(s) <= set("|-+ "):
            continue  # 分隔行（orgtbl 的 |----+----| 行）
        if tables[current]["headers"] is None:
            tables[current]["headers"] = cells
        else:
            tables[current]["rows"].append(cells)
    return tables


def get_combined_default():
    r = run_cli("-l", FIX / "combined.log", "--no-follow")
    assert r.returncode == 0, r.stderr[-400:]
    return r, parse_tables(r.stdout)


def get_access_direct():
    r = run_cli("-f", FMT_MAIN, "-l", FIX / "access.log", "--no-follow")
    assert r.returncode == 0, r.stderr[-400:]
    assert "5 records processed" in r.stdout, r.stdout
    return r, parse_tables(r.stdout)


def col_cell(table, col_name, row=0):
    headers, rows = table["headers"], table["rows"]
    assert headers is not None and rows, "表未解析出表头/数据行"
    idx = headers.index(col_name)
    return rows[row][idx]


def num(x):
    return float(x)


# ---------------- spec-direct（5）----------------


def test_summary_has_median_column():
    # provenance: 请求原文要求输出含 bytes_sent 中位数；Summary 表是默认报表
    # 组成部分。列名取仓库惯例（avg(bytes_sent) AS avg_bytes_sent 的
    # <聚合>_<变量> 命名模式）→ median_bytes_sent。
    _, tables = get_combined_default()
    assert "median_bytes_sent" in tables["Summary"]["headers"], \
        tables["Summary"]["headers"]


def test_detailed_has_median_column():
    # provenance: 默认报表第二张表（Detailed）。既有 bytes_sent 统计列
    # （avg_bytes_sent）在两张表都出现的公开结构 → 中位数列同理。
    _, tables = get_combined_default()
    assert "median_bytes_sent" in tables["Detailed"]["headers"], \
        tables["Detailed"]["headers"]


def test_median_value_summary():
    # provenance: fixture 手算。combined.log（2 行，偶数）：(153+5120)/2=2636.5；
    # access.log（5 行，奇数）：排序 153,300,512,2048,5120 → 512。
    _, t1 = get_combined_default()
    assert abs(num(col_cell(t1["Summary"], "median_bytes_sent")) - 2636.5) < 0.01
    _, t2 = get_access_direct()
    assert abs(num(col_cell(t2["Summary"], "median_bytes_sent")) - 512.0) < 0.01


def test_median_value_per_group():
    # provenance: fixture 手算（access.log 按 request_path 分组）：
    # "/"组（2 行：2048,5120）→ 3584；"/old"→300；"/img/a.png"→512；"/api"→153。
    _, t = get_access_direct()
    got = {}
    for row in t["Detailed"]["rows"]:
        got[row[0]] = num(row[t["Detailed"]["headers"].index("median_bytes_sent")])
    expect = {"/": 3584.0, "/old": 300.0, "/img/a.png": 512.0, "/api": 153.0}
    assert set(got) == set(expect), (got, expect)
    for k, v in expect.items():
        assert abs(got[k] - v) < 0.01, (k, got[k], v)


def test_median_adjacent_to_avg():
    # provenance: DEFAULT_QUERIES 列序惯例——同变量的统计列相邻
    # （新中位数列紧邻既有 avg_bytes_sent）。
    for tables in (get_combined_default()[1], get_access_direct()[1]):
        for name in ("Summary", "Detailed"):
            headers = tables[name]["headers"]
            assert "median_bytes_sent" in headers and "avg_bytes_sent" in headers
            assert abs(headers.index("median_bytes_sent")
                       - headers.index("avg_bytes_sent")) == 1, headers


# ---------------- edge（3，回归保持）----------------


def test_avg_bytes_sent_unchanged():
    # provenance: 冻结公开行为——avg_bytes_sent 列存在且数值正确
    # （combined：2636.5；Detailed 分组：/api=153，/=5120）。
    _, tables = get_combined_default()
    for name in ("Summary", "Detailed"):
        assert "avg_bytes_sent" in tables[name]["headers"], name
    assert abs(num(col_cell(tables["Summary"], "avg_bytes_sent")) - 2636.5) < 0.01
    for row in tables["Detailed"]["rows"]:
        v = num(row[tables["Detailed"]["headers"].index("avg_bytes_sent")])
        assert v in (153.0, 5120.0), row


def test_status_count_columns_unchanged():
    # provenance: 冻结公开行为——2xx/3xx/4xx/5xx 计数列存在且数值正确
    # （access.log Summary：2/1/1/1）。
    _, tables = get_access_direct()
    headers = tables["Summary"]["headers"]
    for c in ("2xx", "3xx", "4xx", "5xx"):
        assert c in headers, headers
    vals = {c: num(col_cell(tables["Summary"], c)) for c in ("2xx", "3xx", "4xx", "5xx")}
    assert vals == {"2xx": 2.0, "3xx": 1.0, "4xx": 1.0, "5xx": 1.0}, vals


def test_default_grouping_unchanged():
    # provenance: 冻结公开行为——Detailed 默认按 request_path 分组
    # （/、/old、/img/a.png、/api；计数 2/1/1/1）。
    _, tables = get_access_direct()
    got = {row[0]: num(row[tables["Detailed"]["headers"].index("count")])
           for row in tables["Detailed"]["rows"]}
    expect = {"/": 2.0, "/old": 1.0, "/img/a.png": 1.0, "/api": 1.0}
    assert got == expect, got
