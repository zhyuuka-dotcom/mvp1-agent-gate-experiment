#!/usr/bin/env bash
# T2 六连跑（GLM 02:10 启动授权）：flash×{A,C,E}×{15,30} 一批，零干预；
# API 三连败=运行完整性事故 → 停批上报（不静默重跑）。
set -u
cd "$(dirname "$0")/../.."
R=/home/z/my-project/learnhub/lab/mvp1/runs/T2
LOG=/tmp/t2-batch.log
run_one() {
  local arm="$1" cap="$2"
  local root="/tmp/t2${arm,,}${cap}"
  echo "=== T2 ${arm}@${cap} START $(date +%T) ===" | tee -a "$LOG"
  if ! python3 runs/T2/run_t2.py "$arm" "$root" "$cap" >> "$LOG" 2>&1; then
    echo "!!! T2 ${arm}@${cap} 事故退出（运行完整性事故——停批上报）" | tee -a "$LOG"
    exit 9
  fi
  echo "=== T2 ${arm}@${cap} END $(date +%T) ===" | tee -a "$LOG"
}
run_one A 15
run_one C 15
run_one E 15
run_one A 30
run_one C 30
run_one E 30
echo "=== BATCH DONE $(date +%T) ===" | tee -a "$LOG"
