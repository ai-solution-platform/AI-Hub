#!/usr/bin/env bash
# pre-edit-lint.sh — Pre-Edit Lint Gate · I-NEW-2
#
# Wraps vm-canonical-lint.py for use as git pre-commit hook OR manual
# save-time gate. Blocks save/commit if V/M divergence detected.
#
# Usage:
#   ./pre-edit-lint.sh <file-path>     # check single file
#   ./pre-edit-lint.sh --all           # full workspace sweep
#   ./pre-edit-lint.sh --staged        # check git-staged files only (pre-commit mode)
#
# Exit codes:
#   0 = clean (allow save/commit)
#   1 = defects found (BLOCK save/commit)
#   2 = error (SSOT missing, etc.)
#
# Activate as git pre-commit hook:
#   chmod +x scripts/pre-edit-lint.sh scripts/vm-canonical-lint.py
#   ln -s ../../scripts/pre-edit-lint.sh .git/hooks/pre-commit

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(dirname "$SCRIPT_DIR")"
LINT_PY="$SCRIPT_DIR/vm-canonical-lint.py"

# Pretty colors
R='\033[31m'
G='\033[32m'
Y='\033[33m'
B='\033[34m'
N='\033[0m'

if [[ ! -f "$LINT_PY" ]]; then
  echo -e "${R}❌ Lint script not found at $LINT_PY${N}"
  exit 2
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo -e "${R}❌ python3 not found in PATH${N}"
  exit 2
fi

if [[ $# -eq 0 ]]; then
  cat <<EOF
Usage:
  $0 <file-path>   # check single file
  $0 --all         # full workspace sweep
  $0 --staged      # check git-staged files (pre-commit mode)
EOF
  exit 2
fi

MODE="$1"
EXIT=0

case "$MODE" in
  --all)
    echo -e "${B}🔎 Pre-Edit Lint Gate · full workspace sweep${N}"
    python3 "$LINT_PY" --strict --no-report || EXIT=$?
    ;;

  --staged)
    echo -e "${B}🔎 Pre-Edit Lint Gate · staged files only${N}"
    if ! command -v git >/dev/null 2>&1; then
      echo -e "${R}❌ git not found · cannot use --staged mode${N}"
      exit 2
    fi
    STAGED=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(html?|md)$' || true)
    if [[ -z "$STAGED" ]]; then
      echo -e "${G}✅ No HTML/MD files staged · pre-commit pass-through${N}"
      exit 0
    fi
    while IFS= read -r f; do
      [[ -z "$f" ]] && continue
      echo -e "${B}── $f${N}"
      python3 "$LINT_PY" --strict --no-report "$WORKSPACE/$f" || EXIT=1
    done <<< "$STAGED"
    ;;

  *)
    if [[ ! -f "$MODE" && ! -f "$WORKSPACE/$MODE" ]]; then
      echo -e "${R}❌ File not found: $MODE${N}"
      exit 2
    fi
    echo -e "${B}🔎 Pre-Edit Lint Gate · $MODE${N}"
    python3 "$LINT_PY" --strict --no-report "$MODE" || EXIT=$?
    ;;
esac

if [[ $EXIT -ne 0 ]]; then
  echo ""
  echo -e "${R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
  echo -e "${R}❌ ❌ ❌  PRE-EDIT LINT GATE BLOCKED THIS SAVE  ❌ ❌ ❌${N}"
  echo -e "${R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
  echo ""
  echo -e "${Y}Canonical fact divergence detected. To unblock:${N}"
  echo ""
  echo "  1. Read /canonical/canonical-facts.md to see canonical truth"
  echo "  2. If your edits introduce a NEW canonical fact:"
  echo "     → update /canonical/vm-status.json AND canonical-facts.md FIRST"
  echo "     → atomic commit · then re-attempt this edit"
  echo "  3. If your edits should align to EXISTING canonical:"
  echo "     → fix the file to match canonical truth"
  echo "  4. Re-run: $0 $MODE"
  echo ""
  echo -e "${Y}Reference (Op Principle 16):${N} Cross-Doc SSOT Discipline · Pattern A"
  echo ""
  exit 1
fi

echo ""
echo -e "${G}✅ Pre-Edit Lint Gate clean — save/commit allowed.${N}"
exit 0
