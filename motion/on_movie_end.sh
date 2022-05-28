#!/usr/bin/env bash

set -eu

echo "Stopping audio recording: $1"
ARECORD_PID_FILE="$1.pid"
ARECORD_PID=$(cat "$ARECORD_PID_FILE")
kill -s SIGINT "$ARECORD_PID"
echo "Audio recording stopped: $1"

# TODO
# 1. Merge video & audio
# 2. Move to the target directory
# 3. Remove source files
