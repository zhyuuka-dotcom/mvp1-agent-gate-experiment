#!/usr/bin/env bash
# T3 六连跑（GLM 03:30 放行）：flash×{A,C,E}×{15,30} 一批，零干预；
# API 三连败=运行完整性事故→停批上报。
set -u
cd "$(dirname "$0")/../.."
LOG=/tmp/t3-batch.log
run_one() {
  local arm="$1" cap="$2"
  echo "=== T3 ${arm}@${cap} START $(date +%T) ===" | tee -a "$LOG"
  if ! python3 runs/T3/run_t3.py "$arm" "/tmp/t3${arm,,}${cap}" "$cap" >> "$LOG" 2>&1; then
    echo "!!! T3 ${arm}@${cap} 事故退出——停批上报" | tee -a "$LOG"
    exit 9
  fi
  echo "=== T3 ${arm}@${cap} END $(date +%T) ===" | tee -a "$LOG"
}
run_one A 15
run_one C 15
run_one E 15
run_one A 30
run_one C 30
run_one E 30
echo "=== T3 BATCH DONE $(date +%T) ===" | tee -a "$LOG"
