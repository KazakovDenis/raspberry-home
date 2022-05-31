#!/usr/bin/env bash

set -eu

NAME=${1%.*}
VIDEO_FILE="$1"
AUDIO_FILE="$NAME.wav"

echo "Stopping audio recording: $AUDIO_FILE"
ARECORD_PID_FILE="$AUDIO_FILE.pid"
ARECORD_PID=$(cat "$ARECORD_PID_FILE")
kill -s SIGINT "$ARECORD_PID"
echo "Audio recording stopped: $AUDIO_FILE"

echo "Merging video & audio: $NAME"
MERGED="$NAME.merged.mkv"
ffmpeg -i "$VIDEO_FILE" -i "$AUDIO_FILE" -c copy "$MERGED"
echo "Merged: $MERGED"

# echo "Moving result: $MERGED"
# REMOTE="remote:motion/"
# rclone move "$MERGED" "$REMOTE"

echo "Removing sources: $VIDEO_FILE, $AUDIO_FILE"
rm "$VIDEO_FILE" "$AUDIO_FILE"
echo "Done: $MERGED"
