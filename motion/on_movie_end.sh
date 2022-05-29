#!/usr/bin/env bash

set -eu

echo "Stopping audio recording: $1"
ARECORD_PID_FILE="$1.pid"
ARECORD_PID=$(cat "$ARECORD_PID_FILE")
kill -s SIGINT "$ARECORD_PID"
echo "Audio recording stopped: $1"

echo "Merging video & audio: $1"
MERGED="$1.merged.mkv"
ffmpeg -i "$1" -i "$1.wav" -c copy "$MERGED"
echo "Merged: $1"

# echo "Moving result: $1"
# mv "$MERGED" .

echo "Removing sources: $1"
rm "$1" "$1.wav"
