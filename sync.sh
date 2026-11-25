#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="${SCRIPT_DIR}/scripts/sync_skills.py"

if [[ -x "${SCRIPT_DIR}/.venv/bin/python" ]] && "${SCRIPT_DIR}/.venv/bin/python" -c "import sys" >/dev/null 2>&1; then
  exec "${SCRIPT_DIR}/.venv/bin/python" "${SCRIPT_PATH}" "$@"
elif command -v python3 >/dev/null 2>&1 && python3 -c "import sys" >/dev/null 2>&1; then
  exec python3 "${SCRIPT_PATH}" "$@"
elif command -v python >/dev/null 2>&1 && python -c "import sys" >/dev/null 2>&1; then
  exec python "${SCRIPT_PATH}" "$@"
elif command -v uv >/dev/null 2>&1; then
  exec uv run --project "${SCRIPT_DIR}" python "${SCRIPT_PATH}" "$@"
else
  echo "[ERROR] Python 3.12+ not found. Please install Python 3 or uv." >&2
  exit 1
fi
