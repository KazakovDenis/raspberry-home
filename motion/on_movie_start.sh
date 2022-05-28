#!/usr/bin/env bash

set -eu

echo "Start audio recording: $FILENAME"
FILENAME="$1.wav"
PID_FILE="$1.pid"
DEVICE="plughw:1,0"
RATE=44100
CHANNELS=2
arecord -f S16_LE -c $CHANNELS -r $RATE --device=$DEVICE --process-id-file "$PID_FILE" "$FILENAME"
