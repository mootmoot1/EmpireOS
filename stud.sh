#!/usr/bin/env bash
set -e
cmd="$1"; shift || true
case "$cmd" in
  upgrade)
    git pull --rebase origin main
    docker compose up -d --build
    python3 devbot/jarvis_devbot.py --test
    ;;
  loop)
    mkdir -p logs
    nohup python3 devbot/jarvis_devbot.py --once >/dev/null 2>&1 || true
    nohup python3 devbot/jarvis_devbot.py --test  >/dev/null 2>&1 || true
    nohup python3 devbot/jarvis_devbot.py        > logs/devbot_health.log 2>&1 &
    echo "DevBot loop started (logs/devbot_health.log)"
    ;;
  repair)
    python3 devbot/jarvis_devbot.py --once
    ;;
  status)
    echo "Containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo; echo "DevBot health (last 20 lines):"
    [ -f logs/devbot_health.log ] && tail -n 20 logs/devbot_health.log || echo "no log yet"
    ;;
  *)
    echo "Usage: ./stud.sh {upgrade|loop|repair|status}"; exit 1 ;;
esac
