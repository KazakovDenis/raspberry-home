#!/usr/bin/env bash

set -eu

NAME=${1%.*}
AUDIO_FILE="$NAME.wav"

echo "Start audio recording: $AUDIO_FILE"
PID_FILE="$AUDIO_FILE.pid"
DEVICE="plughw:1,0"
RATE=44100
CHANNELS=2
arecord -f S16_LE -c $CHANNELS -r $RATE --device=$DEVICE --process-id-file "$PID_FILE" "$AUDIO_FILE"
