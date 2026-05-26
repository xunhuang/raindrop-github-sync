#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SYNC=auto
ANALYZE=1
ENRICH=1
FORCE=0
LIMIT=""

usage() {
  cat <<'EOF'
Usage: ./scripts/run-poi-workflow.sh [options]

Options:
  --sync            Require Raindrop sync before analysis.
  --skip-sync       Do not run Raindrop sync.
  --skip-analyze    Do not run video download/transcription/OCR.
  --skip-enrich     Do not run enrichment.
  --force           Reanalyze successful bookmarks.
  --limit N         Process only the first N bookmarks during analysis.
  -h, --help        Show this help.

Environment:
  RAINDROP_TOKEN          Required only when sync runs.
  RAINDROP_COLLECTION_ID  Optional collection id; defaults to 0 in sync script.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --sync)
      SYNC=require
      shift
      ;;
    --skip-sync)
      SYNC=skip
      shift
      ;;
    --skip-analyze)
      ANALYZE=0
      shift
      ;;
    --skip-enrich)
      ENRICH=0
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --limit)
      LIMIT="${2:-}"
      if [ -z "$LIMIT" ]; then
        echo "--limit requires a number" >&2
        exit 2
      fi
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1. Run ./scripts/setup-local.sh first." >&2
    exit 1
  fi
}

need python3
need jq

if [ "$SYNC" = "require" ] || { [ "$SYNC" = "auto" ] && [ -n "${RAINDROP_TOKEN:-}" ]; }; then
  if [ -z "${RAINDROP_TOKEN:-}" ]; then
    echo "RAINDROP_TOKEN is required for sync." >&2
    exit 1
  fi
  need node
  echo "Syncing Raindrop bookmarks..."
  node scripts/sync-raindrop.mjs
else
  echo "Skipping Raindrop sync."
fi

if [ "$ANALYZE" = "1" ]; then
  need yt-dlp
  need ffmpeg
  need ffprobe
  need tesseract

  args=()
  if [ "$FORCE" = "1" ]; then
    args+=(--force)
  fi
  if [ -n "$LIMIT" ]; then
    args+=(--limit "$LIMIT")
  fi

  echo "Running POI video analysis..."
  python3 scripts/analyze-poi-videos.py "${args[@]}"
else
  echo "Skipping video analysis."
fi

if [ "$ENRICH" = "1" ]; then
  echo "Running POI enrichment..."
  python3 scripts/enrich-poi-analyses.py
else
  echo "Skipping enrichment."
fi

echo "Validating wiki contact sheet links..."
python3 - <<'PY'
from pathlib import Path
import re
base = Path("raindrop/poi-analysis")
wiki = base / "wiki-index.md"
if not wiki.exists():
    raise SystemExit("Missing raindrop/poi-analysis/wiki-index.md")
md = wiki.read_text()
missing = [p for p in re.findall(r"\]\(([^)]*contact_sheet\.jpg)\)", md) if not (base / p).exists()]
if missing:
    raise SystemExit("Missing contact sheet links: " + ", ".join(missing))
print(f"wiki ok: {wiki}")
PY

echo "Done. Open raindrop/poi-analysis/wiki-index.md"
