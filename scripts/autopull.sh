#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
git fetch origin main >/dev/null 2>&1 || exit 0
LOCAL=$(git rev-parse HEAD); REMOTE=$(git rev-parse origin/main); BASE=$(git merge-base HEAD origin/main)
if [ "$REMOTE" != "$LOCAL" ] && [ "$BASE" = "$LOCAL" ]; then
  echo "[autopull] Fast-forwarding main..."; git checkout main >/dev/null 2>&1 || true
  git pull --ff-only origin main
  echo "[autopull] Rebuilding containers..."; docker compose up -d --build
  echo "[autopull] Done."
else echo "[autopull] No updates."
fi
