# T2 参考实现（冻结时绿侧验证用，D-013(1)：不得存在于运行时 agent 可见树）

- 形态：单文件补丁 ngxtop/ngxtop.py（patch 见 reference-impl.patch）
- 实现要点：
  1. docopt usage 新增 `--output-format <fmt>` 选项（默认 table）
  2. SQLProcessor.__init__ 接 output_format 参数；report() 增 json 分支：
     状态行写 stderr，两查询结果按 cursor.description 组装
     {"summary": {...}, "detailed": [...]} 后 json.dumps 输出 stdout
  3. build_processor 末尾校验取值（非 table/json → error_exit 干净报错）
     并传参
- 验证（runs/T2/freeze-verification/）：绿侧 8/8（green-side-reference.txt）；
  存量 28/28（t2-existing.txt）；红侧（无特性基线）4 红 1 空真 3 绿
  （red-side-pristine.txt——invalid 测试空真：docopt 拒未知选项与规格
  拒非法值同可观测行为，如实记录）
- T1 惯例延续：本补丁仅存于 runs/（harness 侧），repo_frozen 冻结树
  不含此实现；agent 运行副本由 repo_frozen 复制，结构上不可见
