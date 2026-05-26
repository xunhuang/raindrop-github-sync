#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

missing=()

has() {
  command -v "$1" >/dev/null 2>&1
}

note() {
  printf '%s\n' "$*"
}

install_macos() {
  if ! has brew; then
    note "Homebrew is not installed. Install it from https://brew.sh, then rerun this script."
    return 1
  fi

  brew update
  brew install yt-dlp ffmpeg tesseract jq node python || true
}

install_linux_apt() {
  sudo apt-get update
  sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    jq \
    ffmpeg \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-chi-sim \
    tesseract-ocr-chi-tra \
    yt-dlp
}

setup_whisper() {
  if has whisper; then
    note "whisper already available: $(command -v whisper)"
    return 0
  fi

  if has pipx; then
    note "Installing openai-whisper with pipx..."
    pipx install openai-whisper || true
  elif has python3; then
    note "Creating .venv-whisper and installing openai-whisper..."
    python3 -m venv .venv-whisper
    .venv-whisper/bin/python -m pip install --upgrade pip
    .venv-whisper/bin/python -m pip install openai-whisper
    note "Whisper installed at .venv-whisper/bin/whisper"
  else
    note "python3 is unavailable; skipping Whisper install."
  fi
}

case "$(uname -s)" in
  Darwin)
    note "Detected macOS."
    install_macos || true
    ;;
  Linux)
    if has apt-get; then
      note "Detected Linux with apt-get."
      install_linux_apt || true
    else
      note "Linux detected, but apt-get is unavailable. Install yt-dlp, ffmpeg, tesseract, jq, node, and python3 manually."
    fi
    ;;
  *)
    note "Unsupported OS for automatic install. Install yt-dlp, ffmpeg, tesseract, jq, node, and python3 manually."
    ;;
esac

for cmd in yt-dlp ffmpeg ffprobe tesseract jq node python3; do
  if ! has "$cmd"; then
    missing+=("$cmd")
  fi
done

if [ "${INSTALL_WHISPER:-1}" != "0" ]; then
  setup_whisper
else
  note "Skipping Whisper install because INSTALL_WHISPER=0."
fi

if [ "${#missing[@]}" -gt 0 ]; then
  note "Missing required commands: ${missing[*]}"
  exit 1
fi

note "Setup complete."
note "Next: export RAINDROP_TOKEN if you want to sync, then run ./scripts/run-poi-workflow.sh"
