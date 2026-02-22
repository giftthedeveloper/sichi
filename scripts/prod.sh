#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_DIR="$BACKEND_DIR/.venv"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required"
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating backend virtualenv..."
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

if ! python -c "import fastapi, uvicorn, requests" >/dev/null 2>&1; then
  echo "Installing backend dependencies..."
  pip install -r "$BACKEND_DIR/requirements.txt"
fi

export BUN_INSTALL="${BUN_INSTALL:-$HOME/.bun}"
export PATH="$BUN_INSTALL/bin:$PATH"

if ! command -v bun >/dev/null 2>&1; then
  echo "bun is required"
  exit 1
fi

echo "Starting backend on http://0.0.0.0:8000"
(
  cd "$BACKEND_DIR"
  uvicorn app.main:app --host 0.0.0.0 --port 8000
) &
BACKEND_PID=$!

cleanup() {
  if kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    kill "$BACKEND_PID"
  fi
}
trap cleanup EXIT INT TERM

echo "Starting frontend preview on http://0.0.0.0:4173"
cd "$ROOT_DIR"
bun run preview --host 0.0.0.0 --port 4173
