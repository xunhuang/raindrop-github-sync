#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/skills/poi-video-analysis"
DEST="${CODEX_HOME:-$HOME/.codex}/skills/poi-video-analysis"

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "Missing skill source: $SRC/SKILL.md" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"

echo "Installed Codex skill:"
echo "$DEST"
echo
echo "In a new Codex session, ask:"
echo "Use the poi-video-analysis skill to analyze this repo's bookmarks and update the wiki index."
