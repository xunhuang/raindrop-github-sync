#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKMARKS = ROOT / "raindrop" / "bookmarks.json"
OUT_ROOT = ROOT / "raindrop" / "poi-analysis"
YTDLP = shutil.which("yt-dlp") or "/opt/homebrew/bin/yt-dlp"
FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
WHISPER = shutil.which("whisper") or str(Path.home() / ".local" / "bin" / "whisper")
TESSERACT = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"


def run(cmd, cwd=ROOT, timeout=600, capture=True):
    kwargs = {
        "cwd": cwd,
        "timeout": timeout,
        "text": True,
    }
    if capture:
        kwargs.update({"stdout": subprocess.PIPE, "stderr": subprocess.PIPE})
    proc = subprocess.run(cmd, **kwargs)
    if proc.returncode != 0:
        msg = proc.stderr.strip() if capture and proc.stderr else f"exit {proc.returncode}"
        raise RuntimeError(msg)
    return proc.stdout if capture else ""


def safe_name(text):
    text = re.sub(r"https?://", "", text or "")
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-")
    return text[:64] or "bookmark"


def bookmark_dir(item):
    key = str(item.get("_id") or hashlib.sha1(item["link"].encode()).hexdigest()[:12])
    return OUT_ROOT / f"{key}-{safe_name(item.get('domain') or item.get('title') or item['link'])}"


def load_json(path, default=None):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return default


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def existing_success(out_dir, source_url):
    data = load_json(out_dir / "analysis.json", {})
    ok = data.get("status") == "success" and data.get("source_url") == source_url
    if ok:
        (out_dir / "error.txt").unlink(missing_ok=True)
    return ok


def discover_video(out_dir):
    for path in sorted(out_dir.glob("*.mp4")):
        if path.name != "contact_sheet.mp4":
            return path
    for path in sorted(out_dir.glob("*.mkv")):
        return path
    return None


def download(item, out_dir):
    video = discover_video(out_dir)
    info_files = list(out_dir.glob("*.info.json"))
    if video and info_files:
        return video, info_files[0]

    output = str(out_dir / "source.%(ext)s")
    cmd = [
        YTDLP,
        "--no-playlist",
        "--no-mtime",
        "--socket-timeout",
        "30",
        "--retries",
        "2",
        "--extractor-retries",
        "2",
        "--write-info-json",
        "-f",
        "bv*[height<=720]+ba/b[height<=720]/best",
        "-o",
        output,
        item["link"],
    ]
    run(cmd, timeout=900, capture=True)
    video = discover_video(out_dir)
    info_files = list(out_dir.glob("*.info.json"))
    if not video:
        raise RuntimeError("yt-dlp completed but no video file was produced")
    return video, info_files[0] if info_files else None


def media_duration(path):
    try:
        out = run(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            timeout=60,
        )
        return float(out.strip())
    except Exception:
        return None


def extract_audio(video, out_dir):
    audio = out_dir / "audio.wav"
    if audio.exists() and audio.stat().st_size > 0:
        return audio
    run([FFMPEG, "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(audio)], timeout=300)
    return audio


def transcribe(audio, out_dir):
    transcript = out_dir / "audio.txt"
    if transcript.exists() and transcript.stat().st_size > 0:
        return transcript.read_text(errors="replace").strip()
    if not Path(WHISPER).exists() and not shutil.which("whisper"):
        return ""
    cmd = [
        WHISPER,
        str(audio),
        "--model",
        "small",
        "--language",
        "Chinese",
        "--task",
        "transcribe",
        "--output_format",
        "txt",
        "--output_dir",
        str(out_dir),
    ]
    run(cmd, timeout=1800, capture=True)
    generated = out_dir / f"{audio.stem}.txt"
    if generated.exists() and generated != transcript:
        generated.rename(transcript)
    return transcript.read_text(errors="replace").strip() if transcript.exists() else ""


def extract_frames(video, out_dir, duration):
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    if list(frames_dir.glob("frame_*.jpg")):
        return sorted(frames_dir.glob("frame_*.jpg"))
    every = 2 if not duration or duration <= 90 else 4
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            str(video),
            "-vf",
            f"fps=1/{every},scale=360:-1",
            "-q:v",
            "3",
            str(frames_dir / "frame_%03d.jpg"),
        ],
        timeout=300,
    )
    frames = sorted(frames_dir.glob("frame_*.jpg"))
    if frames:
        run(
            [
                FFMPEG,
                "-y",
                "-pattern_type",
                "glob",
                "-i",
                str(frames_dir / "frame_*.jpg"),
                "-vf",
                "tile=4x4:padding=8:margin=8",
                "-frames:v",
                "1",
                str(out_dir / "contact_sheet.jpg"),
            ],
            timeout=120,
        )
    return frames


def ocr_frames(frames, out_dir):
    ocr_path = out_dir / "visible_text.txt"
    if ocr_path.exists() and ocr_path.stat().st_size > 0:
        return ocr_path.read_text(errors="replace").strip()
    if not frames:
        return ""
    lines = []
    for frame in frames[:40]:
        try:
            text = run([TESSERACT, str(frame), "stdout", "-l", "chi_tra+chi_sim+eng", "--psm", "6"], timeout=60)
        except Exception:
            continue
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        if text:
            lines.append(f"## {frame.name}\n{text}")
    result = "\n\n".join(lines).strip()
    ocr_path.write_text(result + ("\n" if result else ""))
    return result


def compact_text(text, max_chars=3000):
    text = re.sub(r"\n{3,}", "\n\n", text or "").strip()
    return text if len(text) <= max_chars else text[:max_chars].rstrip() + "\n[truncated]"


def infer_place(item, info):
    text = "\n".join(
        str(x or "")
        for x in [
            item.get("title"),
            item.get("excerpt"),
            info.get("title"),
            info.get("description"),
            info.get("uploader"),
        ]
    )
    patterns = [
        r"📍\s*([^#\n]+)",
        r"🔅\s*([^#\n]+)",
        r"(黑木亭[^#\n]*)",
        r"(Maguro Mart)",
        r"(鮨冠[^#\n]*)",
        r"(壽司宋[^#\n]*)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            return m.group(1).strip()
    return item.get("title") or info.get("title") or item["link"]


def make_markdown(item, info, transcript, visible_text, duration, status_note=""):
    comments = info.get("comments") or info.get("comment") or []
    comment_text = "No public comments were exposed by yt-dlp for this URL."
    if isinstance(comments, list) and comments:
        comment_text = "\n".join(f"- {c.get('text') or c}" for c in comments[:20])

    description = item.get("title") or info.get("description") or info.get("title") or ""
    if info.get("description") and info.get("description") != description:
        description += "\n\n" + info.get("description")

    place = infer_place(item, info)
    gist_parts = []
    if description:
        gist_parts.append(description)
    if transcript:
        gist_parts.append("Audio transcript suggests: " + transcript[:700])
    if visible_text:
        gist_parts.append("Visible text/OCR suggests: " + re.sub(r"\s+", " ", visible_text)[:900])
    gist = "\n\n".join(gist_parts)

    return f"""# {place}

Source: {item["link"]}

Bookmark id: {item.get("_id", "")}
Analyzed: {datetime.now(timezone.utc).isoformat()}

## Download / Metadata

- Status: success{status_note}
- Platform/domain: {item.get("domain", "")}
- Uploader: {info.get("uploader") or info.get("channel") or ""}
- Upload date: {info.get("upload_date") or ""}
- Duration: {duration or info.get("duration") or ""}
- View count: {info.get("view_count") or ""}
- Like/reaction count: {info.get("like_count") or info.get("repost_count") or ""}

## Description

{compact_text(description, 2500) or "No description text was available."}

## Comments

{compact_text(comment_text, 2500)}

## Gist

{compact_text(gist, 3500) or "The script could not infer a detailed gist from available metadata, OCR, or audio."}

## Audio Transcript

{compact_text(transcript, 5000) or "No speech transcript was produced."}

## Visible Text / Video OCR

{compact_text(visible_text, 5000) or "No visible text was detected from sampled frames."}
"""


def analyze_one(item, force=False):
    out_dir = bookmark_dir(item)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not force and existing_success(out_dir, item["link"]):
        print(f"skip success: {out_dir.name}")
        return "skipped"

    manifest = {
        "status": "started",
        "source_url": item["link"],
        "bookmark_id": item.get("_id"),
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(out_dir / "analysis.json", manifest)
    try:
        video, info_path = download(item, out_dir)
        info = load_json(info_path, {}) if info_path else {}
        duration = media_duration(video)
        audio = extract_audio(video, out_dir)
        transcript = transcribe(audio, out_dir)
        frames = extract_frames(video, out_dir, duration)
        visible_text = ocr_frames(frames, out_dir)
        md = make_markdown(item, info, transcript, visible_text, duration)
        (out_dir / "analysis.md").write_text(md)
        manifest.update(
            {
                "status": "success",
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "video": video.name,
                "info_json": info_path.name if info_path else None,
                "duration": duration,
                "analysis_markdown": "analysis.md",
            }
        )
        (out_dir / "error.txt").unlink(missing_ok=True)
        write_json(out_dir / "analysis.json", manifest)
        print(f"success: {out_dir.name}")
        return "success"
    except Exception as exc:
        manifest.update(
            {
                "status": "failed",
                "failed_at": datetime.now(timezone.utc).isoformat(),
                "error": str(exc),
            }
        )
        write_json(out_dir / "analysis.json", manifest)
        (out_dir / "error.txt").write_text(str(exc) + "\n")
        print(f"failed: {out_dir.name}: {exc}", file=sys.stderr)
        return "failed"


def main():
    parser = argparse.ArgumentParser(description="Download and analyze Raindrop POI videos idempotently.")
    parser.add_argument("--force", action="store_true", help="reanalyze even if analysis.json is already successful")
    parser.add_argument("--limit", type=int, default=0, help="process only the first N bookmarks")
    args = parser.parse_args()

    items = json.loads(BOOKMARKS.read_text())
    if args.limit:
        items = items[: args.limit]
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    counts = {"success": 0, "failed": 0, "skipped": 0}
    for item in items:
        result = analyze_one(item, force=args.force)
        counts[result] += 1
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
