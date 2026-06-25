#!/bin/bash
# Run this from the repo root to sync with remote, then push your local commits.
# Usage: bash pull-then-push.sh

cd "$(dirname "$0")"

echo "Pulling remote changes (rebase)..."
git pull --rebase origin main

if [ $? -ne 0 ]; then
  echo ""
  echo "ERROR: pull --rebase failed. Check for merge conflicts above."
  exit 1
fi

echo ""
echo "Push is now safe — go ahead and push from Sourcetree."
echo "(Or run: git push origin main)"
