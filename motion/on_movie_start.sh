#!/usr/bin/env bash

set -eu

FILENAME="$1.wav"
PID_FILE="$1.pid"
DEVICE="plughw:1,0"
RATE=44100
CHANNELS=2
DURATION=60

echo "Start audio recording: $FILENAME"
arecord -f S16_LE -d $DURATION -c $CHANNELS -r $RATE --device=$DEVICE --process-id-file "$PID_FILE" "$FILENAME"
