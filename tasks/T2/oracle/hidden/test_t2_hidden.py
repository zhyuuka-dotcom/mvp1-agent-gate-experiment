"""T2 隐藏验收（MVP-1 神谕草稿——盲态保护中，D-006）。

状态：本目录未推送至公开仓（D-006 盲态保护条款）；推导清单存档并匹配
审计通过后随 T2 冻结 commit 入库。Agent 永远不可见本文件。

类别：spec-direct = 任务规格（Benchmark-authored 规格 bullet 1-7 与验收例
      1-3）派生的必要条件；edge = 冻结时公开行为派生的边界/回归条件。
每条 provenance 注明派生来源（规格 bullet/验收例编号）。
全部断言只依赖：task.md 规格 + 验收例 + oracle 侧 fixture 副本。

运行方式：MVP1_REPO=<agent 工作副本绝对路径> python -m pytest 本文件
（fixture 用 oracle 侧副本路径调用 agent 的 CLI——内容与冻结 repro
逐字节一致；agent 改动其工作副本内 repro/ 不影响神谕判定）
"""
import json
import os
import re
import subprocess
from pathlib import Path

REPO = Path(os.environ["MVP1_REPO"]).resolve()
PY = REPO / ".venv/bin/python"
ORACLE = Path(__file__).resolve().parent.parent  # tasks/T2/oracle/
FIX = ORACLE  # T2 oracle 侧 fixture 副本就放在 oracle/ 根下

# issue 格式串（repro/nginx.conf log_format main 内容逐字；验收例 2 命令同款）
FMT_MAIN = ('$request_time $upstream_response_time $remote_addr - $upstream_addr '
            '[$time_local] $host "$request" $status $bytes_sent '
            '"$http_referer" "$http_user_agent" "$gzip_ratio" '
            '"$http_x_forwarded_for" - "$server_addr"')


def run_cli(*args):
    return subprocess.run([str(PY), "-m", "ngxtop.ngxtop", *map(str, args)],
                          cwd=str(REPO), capture_output=True, text=True,
                          timeout=120)


def run_json(*args):
    r = run_cli(*args, "--output-format", "json")
    assert r.returncode == 0, r.stderr[-400:]
    return r, json.loads(r.stdout)


def parse_tables(stdout):
    """把 orgtbl 输出解析为 {节名: {"headers": [...], "rows": [[...]]}}。"""
    tables, current = {}, None
    for line in stdout.splitlines():
        s = line.strip()
        if s in ("Summary:", "Detailed:"):
            current = s[:-1]
            tables[current] = {"headers": None, "rows": []}
            continue
        if current is None or not s.startswith("|"):
            continue
        if set(s) <= set("|-+ "):
            continue  # 分隔行
        cells = [c.strip() for c in s.strip("|").split("|")]
        if tables[current]["headers"] is None:
            tables[current]["headers"] = cells
        else:
            tables[current]["rows"].append(cells)
    return tables


def num(x):
    return float(x)


def approx(a, b, tol=0.01):
    return abs(float(a) - float(b)) <= tol


# ---------------- spec-direct（5）----------------


def test_json_structure_and_stdout_purity():
    # provenance: 规格 bullet 3/4 + 验收例 1——stdout 恰含一个合法 JSON 文档，
    # 顶层恰有 summary/detailed 两键；状态行在 stderr 不在 stdout。
    r, doc = run_json("-l", FIX / "combined.log", "--no-follow")
    assert set(doc.keys()) == {"summary", "detailed"}, doc.keys()
    assert "records processed" not in r.stdout, r.stdout  # stdout 无状态行
    assert "records processed" in r.stderr, r.stderr  # 状态行在 stderr
    assert isinstance(doc["summary"], dict) and isinstance(doc["detailed"], list)


def test_json_summary_values():
    # provenance: 规格 bullet 4 + 验收例 1/2——summary 键=列名，数值类型，
    # 值与验收例逐值相等（两 fixture 各一次调用）。
    _, doc = run_json("-l", FIX / "combined.log", "--no-follow")
    s = doc["summary"]
    assert set(s.keys()) == {"count", "avg_bytes_sent", "2xx", "3xx", "4xx", "5xx"}, s.keys()
    for k in ("count", "2xx", "3xx", "4xx", "5xx"):
        assert isinstance(s[k], int) and not isinstance(s[k], bool), (k, s[k])
    assert approx(s["avg_bytes_sent"], 2636.5)
    assert (s["count"], s["2xx"], s["3xx"], s["4xx"], s["5xx"]) == (2, 1, 0, 1, 0)
    _, doc2 = run_json("-f", FMT_MAIN, "-l", FIX / "access.log", "--no-follow")
    s2 = doc2["summary"]
    assert approx(s2["avg_bytes_sent"], 1626.6)
    assert (s2["count"], s2["2xx"], s2["3xx"], s2["4xx"], s2["5xx"]) == (5, 2, 1, 1, 1)


def test_json_detailed_values():
    # provenance: 规格 bullet 4 + 验收例 1/2——detailed 行对象键=分组列名+统计
    # 列名，分组值为字符串，行序不作要求（集合语义）；另验 -g 换分组列时
    # 键随分组列（规格 bullet 4"分组列名"的一般化）。
    _, doc = run_json("-l", FIX / "combined.log", "--no-follow")
    rows = doc["detailed"]
    assert len(rows) == 2, rows
    by_g = {r["request_path"]: r for r in rows}
    assert set(by_g.keys()) == {"/", "/api"}
    assert isinstance(by_g["/"]["request_path"], str)
    assert by_g["/"]["count"] == 1 and approx(by_g["/"]["avg_bytes_sent"], 5120.0)
    assert by_g["/api"]["count"] == 1 and approx(by_g["/api"]["avg_bytes_sent"], 153.0)
    _, doc2 = run_json("-f", FMT_MAIN, "-l", FIX / "access.log", "--no-follow")
    by_g2 = {r["request_path"]: r for r in doc2["detailed"]}
    assert set(by_g2.keys()) == {"/", "/old", "/img/a.png", "/api"}
    assert by_g2["/"]["count"] == 2 and approx(by_g2["/"]["avg_bytes_sent"], 3584.0)
    for g in ("/old", "/img/a.png", "/api"):
        assert by_g2[g]["count"] == 1
    assert approx(by_g2["/old"]["avg_bytes_sent"], 300.0)
    assert approx(by_g2["/img/a.png"]["avg_bytes_sent"], 512.0)
    assert approx(by_g2["/api"]["avg_bytes_sent"], 153.0)
    # -g 换分组列：键随分组列名
    _, doc3 = run_json("-g", "remote_addr", "-f", FMT_MAIN, "-l", FIX / "access.log",
                       "--no-follow")
    rows3 = doc3["detailed"]
    assert all("remote_addr" in r for r in rows3), rows3
    by_g3 = {r["remote_addr"]: r for r in rows3}
    assert set(by_g3.keys()) == {"10.0.0.1", "10.0.0.2", "10.0.0.3"}
    assert by_g3["10.0.0.1"]["count"] == 2 and by_g3["10.0.0.2"]["count"] == 2
    assert by_g3["10.0.0.3"]["count"] == 1


def test_table_mode_unchanged():
    # provenance: 规格 bullet 1/2——不传 --output-format 与显式
    # --output-format table 行为相同；输出=状态行+两 orgtbl 表（现行格式）。
    r_def = run_cli("-l", FIX / "combined.log", "--no-follow")
    assert r_def.returncode == 0, r_def.stderr[-400:]
    r_exp = run_cli("-l", FIX / "combined.log", "--no-follow",
                    "--output-format", "table")
    assert r_exp.returncode == 0, r_exp.stderr[-400:]
    for r in (r_def, r_exp):
        assert "records processed" in r.stdout, r.stdout  # 状态行在 stdout
    assert r_def.stdout.splitlines()[1:] == r_exp.stdout.splitlines()[1:], \
        "explicit table 与缺省输出不一致（除首行状态行外逐行相等）"
    tables = parse_tables(r_def.stdout)
    assert set(tables.keys()) == {"Summary", "Detailed"}, tables.keys()
    sh = tables["Summary"]["headers"]
    assert sh == ["count", "avg_bytes_sent", "2xx", "3xx", "4xx", "5xx"], sh
    row = tables["Summary"]["rows"][0]
    assert num(row[sh.index("count")]) == 2 and approx(num(row[sh.index("avg_bytes_sent")]), 2636.5)


def test_invalid_format_rejected():
    # provenance: 规格 bullet 5 + 验收例 3——table/json 之外的取值：
    # stderr 一行错误信息，退出码非 0，stdout 无 JSON。
    r = run_cli("-l", FIX / "combined.log", "--no-follow",
                "--output-format", "yaml")
    assert r.returncode != 0, r.stdout
    assert r.stderr.strip(), "stderr 须有错误信息"
    assert not r.stdout.strip().startswith("{"), r.stdout[:200]


# ---------------- edge（3）----------------


def test_default_combined_tables():
    # provenance: 冻结公开行为——默认 combined 运行：状态行+两表
    # （特征化测试同源；新选项缺席时的行为锚点）。
    r = run_cli("-l", FIX / "combined.log", "--no-follow")
    assert r.returncode == 0, r.stderr[-400:]
    assert "2 records processed" in r.stdout, r.stdout
    tables = parse_tables(r.stdout)
    assert set(tables.keys()) == {"Summary", "Detailed"}
    dh = tables["Detailed"]["headers"]
    assert dh[0] == "request_path" and "count" in dh and "avg_bytes_sent" in dh
    groups = {row[0] for row in tables["Detailed"]["rows"]}
    assert groups == {"/", "/api"}


def test_multi_group_by_unchanged():
    # provenance: 冻结公开行为——`-g a,b` 多列分组已支持（issue #27 已实现），
    # 与直传格式串组合仍须工作。
    r = run_cli("-g", "remote_addr,status", "-f", FMT_MAIN,
                "-l", FIX / "access.log", "--no-follow")
    assert r.returncode == 0, r.stderr[-400:]
    assert "remote_addr" in r.stdout and "status" in r.stdout
    assert "10.0.0.1" in r.stdout and "200" in r.stdout


def test_access_direct_records():
    # provenance: 冻结公开行为——直传格式串+access.log：5 records processed。
    r = run_cli("-f", FMT_MAIN, "-l", FIX / "access.log", "--no-follow")
    assert r.returncode == 0, r.stderr[-400:]
    assert "5 records processed" in r.stdout, r.stdout
