# Raindrop GitHub Sync and POI Video Analysis

This repo syncs Raindrop bookmarks and can turn social/video bookmark URLs into point-of-interest analyses.

The POI workflow downloads videos, extracts metadata/audio/frames, transcribes speech, OCRs visible text, enriches restaurant/travel details, and writes a geography-organized wiki page with inline contact sheets.

## Fresh Machine Setup

On a new computer:

```bash
git clone git@github.com:xunhuang/raindrop-github-sync.git
cd raindrop-github-sync
./scripts/setup-local.sh
./scripts/install-codex-skill.sh
```

Equivalent Makefile shortcuts:

```bash
make setup
make install-skill
```

`setup-local.sh` installs or checks for:

- `yt-dlp`
- `ffmpeg` / `ffprobe`
- `tesseract`
- `jq`
- `node`
- `python3`
- optional local Whisper transcription support

The setup script supports macOS with Homebrew and Debian/Ubuntu-style Linux with `apt-get`. If a dependency manager is unavailable, it prints the missing commands to install manually.

## Required Token for Bookmark Sync

To sync from Raindrop, set:

```bash
export RAINDROP_TOKEN="..."
```

Optional:

```bash
export RAINDROP_COLLECTION_ID="0"
```

If `RAINDROP_TOKEN` is absent, the POI run script can still analyze the existing checked-in `raindrop/bookmarks.json`.

## Run Everything

Use:

```bash
./scripts/run-poi-workflow.sh
```

or:

```bash
make run
```

By default this:

1. Syncs Raindrop only if `RAINDROP_TOKEN` is set.
2. Runs `scripts/analyze-poi-videos.py`.
3. Runs `scripts/enrich-poi-analyses.py`.
4. Validates that `wiki-index.md` inline contact-sheet links resolve.

Useful options:

```bash
./scripts/run-poi-workflow.sh --skip-sync
./scripts/run-poi-workflow.sh --limit 3
./scripts/run-poi-workflow.sh --force
./scripts/run-poi-workflow.sh --skip-analyze
make validate
```

## Outputs

Main wiki:

```text
raindrop/poi-analysis/wiki-index.md
```

Per-bookmark folders:

```text
raindrop/poi-analysis/<bookmark-id>-<domain>/
```

Important files in each successful folder:

- `analysis.md` - human-readable POI writeup
- `analysis.json` - idempotency/status metadata
- `source.info.json` - social/video metadata from `yt-dlp`
- `source.mp4` - downloaded video
- `audio.wav` / `audio.txt` - extracted audio and transcript
- `visible_text.txt` - raw OCR
- `contact_sheet.jpg` - inline visual summary used by the wiki
- `frames/` - sampled frames

## Codex Usage on a New Machine

After running `./scripts/install-codex-skill.sh`, tell Codex:

```text
Use the poi-video-analysis skill to analyze the bookmarks in this repo. Run setup if needed, then run the POI workflow and update the wiki index.
```

The repo-local skill source is:

```text
skills/poi-video-analysis/SKILL.md
```

The installer copies it to:

```text
~/.codex/skills/poi-video-analysis
```

## Large Files

This repo currently stores downloaded media directly in Git. Git LFS is not configured. Before committing new analyses, check file size:

```bash
du -sh raindrop/poi-analysis
find raindrop/poi-analysis -type f -size +50M -print
git lfs version
```

GitHub rejects individual files over 100 MB. Prefer Git LFS or avoid committing full media if future videos become large.
