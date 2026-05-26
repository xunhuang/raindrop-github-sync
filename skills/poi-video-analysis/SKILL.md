---
name: poi-video-analysis
description: Analyze social media/video bookmark URLs into reusable point-of-interest travel and food writeups. Use when Codex needs to process Raindrop bookmarks, Facebook/Instagram/Xiaohongshu/TikTok/video links, downloaded short-form videos, restaurant or attraction posts, POI transcripts, visible-video text, contact sheets, or geography-organized wiki indexes with city/address/price/reservation details.
---

# POI Video Analysis

## Goal

Turn a list of social/video bookmarks into idempotent point-of-interest analyses with enough practical context for travel or food planning. Combine metadata, post text, video/audio transcription, visible text, comments when accessible, and best-effort web lookup.

## Inputs

Prefer these defaults unless the user gives different paths:

- Bookmark source: `raindrop/bookmarks.json`
- Output root: `raindrop/poi-analysis/`
- Per-bookmark output folder: `<bookmark-id>-<domain>/`
- Detailed analysis: `analysis.md`
- Machine status: `analysis.json`
- Geography overview: `wiki-index.md`

Expected bookmark fields include `_id`, `link`, `title`, `excerpt`, `domain`, and `created`.

## Workflow

1. Inspect the repo and current outputs before doing work.
   - Use `rg --files`, `find`, `jq`, and `git status --short`.
   - Preserve unrelated untracked or modified files.

2. Create or reuse an idempotent per-bookmark pipeline.
   - If `analysis.json` has `status: "success"` and the same `source_url`, skip download/transcription for that bookmark.
   - If a previous run failed, retry it unless the user asks not to.
   - Record failures in `analysis.json` and `error.txt` without stopping the batch.

3. Download and extract media.
   - Use `yt-dlp` for metadata and video download.
   - Save `source.info.json` and `source.mp4` when available.
   - Use `ffmpeg`/`ffprobe` to extract `audio.wav`, duration, sampled frames, and `contact_sheet.jpg`.
   - Keep individual files below GitHub limits when the user wants commits. Note when Git LFS is unavailable.

4. Transcribe and read the video.
   - Use local Whisper if available for `audio.txt`.
   - Use Tesseract or direct visual inspection for visible captions, menus, signs, addresses, prices, phone numbers, and calls to action.
   - Store raw OCR in `visible_text.txt`, but write an interpreted summary in `analysis.md`; raw OCR from vertical videos is often noisy.

5. Fetch social metadata and comments.
   - Include post description/title/uploader/upload date/view count when exposed by `yt-dlp`.
   - Try a metadata-only comment probe when appropriate, e.g. `yt-dlp --write-comments --skip-download --dump-json <url>`.
   - If comments are unavailable, explicitly say so. Do not invent comments.

6. Enrich POI details.
   - For restaurants and attractions, perform best-effort lookup for city, district, address, transit, cuisine/genre, price point, and reservation guidance.
   - Use current web lookups when facts can change or when the place is unfamiliar.
   - Prefer official pages and established directories such as OpenRice, TableCheck, Google/Apple Maps snippets, Trip.com, restaurant pages, or venue pages.
   - Cite/link source notes in the analysis.

7. Write each `analysis.md`.
   - Include:
     - POI name
     - source URL
     - bookmark id
     - city, area, address, transit
     - food/experience genre
     - price point
     - whether reservations are needed
     - original post description
     - top comments, or an explicit unavailable-comments note
     - deeper gist from description + transcript + visible/video context + lookups
     - food/experience notes and must-try items
     - interpreted visible text
     - audio transcript
     - raw OCR for traceability
     - source notes

8. Build a geography-organized wiki index.
   - Create or update `raindrop/poi-analysis/wiki-index.md`.
   - Group by city/country, then district or neighborhood.
   - For each successful item, include high-level gist, address, genre, price, reservation note, link to `analysis.md`, and inline `contact_sheet.jpg`.
   - Add sections for `Unknown / Not Enough POI Evidence` and `Failed Analysis`.
   - Verify all image links resolve.

9. Validate and report.
   - Run an idempotency smoke test on at least one completed bookmark.
   - Check for missing contact sheets and broken wiki image paths.
   - Summarize success/failure counts and any remaining blockers.

## Analysis Rules

- Distinguish evidence from inference. Say “best effort” when a city/address/price/reservation note comes from partial evidence.
- Do not treat a recipe/process clip as a POI unless there is a reliable shop/place name.
- Do not invent top comments. If social platforms require login/cookies and comments are not exposed, write that.
- Preserve downloaded media only when the user asked to keep/check in all artifacts. Otherwise, ask or prefer committing analysis markdown, metadata, and contact sheets over full videos/audio.
- If multiple bookmark URLs resolve to the same post/place, either deduplicate in the wiki or cross-link the duplicate source posts.

## Useful Commands

```bash
jq -r '.[].link' raindrop/bookmarks.json
find raindrop/poi-analysis -maxdepth 2 -name analysis.json -print
find raindrop/poi-analysis -maxdepth 2 -name contact_sheet.jpg -print
python3 scripts/analyze-poi-videos.py
python3 scripts/analyze-poi-videos.py --limit 1
python3 scripts/enrich-poi-analyses.py
python3 - <<'PY'
from pathlib import Path
import re
base = Path('raindrop/poi-analysis')
md = (base / 'wiki-index.md').read_text()
missing = [p for p in re.findall(r'\]\(([^)]*contact_sheet\.jpg)\)', md) if not (base / p).exists()]
print('missing:', missing)
PY
```

## Commit Guidance

Before committing:

- Run `git status --short`.
- Inspect large files: `find raindrop/poi-analysis -type f -exec ls -lh {} \; | sort -k5 -hr | sed -n '1,80p'`.
- Check total size: `du -sh raindrop/poi-analysis`.
- Check Git LFS availability: `git lfs version`.
- If Git LFS is unavailable and files are below GitHub limits, say so before pushing.
