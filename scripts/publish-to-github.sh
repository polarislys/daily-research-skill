#!/usr/bin/env bash
# 在你本机、已登录 gh 的终端运行：把当前仓库建成 GitHub 个人仓 daily-research-skill
set -euo pipefail

REPO_NAME="${REPO_NAME:-daily-research-skill}"
VISIBILITY="${VISIBILITY:-private}"

if ! command -v gh >/dev/null 2>&1; then
  echo "需要 GitHub CLI：https://cli.github.com/" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "请先运行：gh auth login" >&2
  exit 1
fi

if gh repo view "$REPO_NAME" >/dev/null 2>&1; then
  echo "仓库已存在，改为添加 remote 并推送。"
else
  gh repo create "$REPO_NAME" --"$VISIBILITY" --source=. --remote=github --push --description "每日 10:00 调研简报（Cloud Agent 产物）"
  echo "已创建并推送：$(gh repo view "$REPO_NAME" --json url -q .url)"
  exit 0
fi

if git remote get-url github >/dev/null 2>&1; then
  git remote set-url github "$(gh repo view "$REPO_NAME" --json url -q .url).git"
else
  git remote add github "$(gh repo view "$REPO_NAME" --json url -q .url).git"
fi

git push -u github HEAD:main
echo "已推送到 $(gh repo view "$REPO_NAME" --json url -q .url)"
