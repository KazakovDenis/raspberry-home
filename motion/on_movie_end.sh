#!/usr/bin/env bash

set -eu

# Stop audio recording
ARECORD_PID_FILE="$1.pid"
ARECORD_PID=$(cat "$ARECORD_PID_FILE")

kill -s SIGTERM "$ARECORD_PID"
echo "Audio recording stopped: $1"

# TODO
# 1. Merge video & audio
# 2. Move to the target directory
# 3. Remove source files
