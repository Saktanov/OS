#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [--top N] <directory> <ERROR|WARN|INFO>"
}

top=""
if [[ "${1:-}" == "--top" ]]; then
  top="${2:-}"
  shift 2
fi

if [[ $# -ne 2 ]]; then
  usage
  exit 1
fi

dir="$1"
level="$2"

if [[ ! -d "$dir" ]]; then
  echo "Directory not found: $dir" >&2
  exit 1
fi

case "$level" in
  ERROR|WARN|INFO) ;;
  *) echo "Level must be ERROR, WARN or INFO" >&2; exit 1 ;;
esac

awk -v level="$level" '
  $3 == level {
    for (i = 1; i <= NF; i++) {
      if ($i ~ /^module=/) {
        sub(/^module=/, "", $i)
        count[$i]++
      }
    }
  }
  END {
    for (m in count) {
      print m, count[m]
    }
  }
' "$dir"/*.log | sort -k2,2nr | {
  if [[ -n "$top" ]]; then
    head -n "$top"
  else
    cat
  fi
}
