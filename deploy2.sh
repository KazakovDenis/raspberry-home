#!/usr/bin/env bash

set -e -u

APP_DIR="/opt/app"
TMP_DIR="/tmp/$(date +%s)"

function output {
    RED="\033[0;31m"
    GREEN="\033[0;32m"
    YELLOW="\033[1;33m"
    NO_COLOR="\033[0m"
    printf "${!1}${2} ${NO_COLOR}\n"
}

output YELLOW "Uploading sources to Raspberry Pi"
ssh raspi "mkdir -p $TMP_DIR"
scp -r -C src raspi:$TMP_DIR
scp docker-compose.yml .env raspi:$TMP_DIR

#ssh raspi "docker compose -f ${TMP_DIR}/docker-compose.yml up -d --build"

output YELLOW "Starting new containers at Raspberry Pi"
ssh raspi <<EOF
  docker compose -f "$TMP_DIR"/docker-compose.yml up -d --build --remove-orphans
  echo "Cleaning up"
  mv -f "$TMP_DIR" "$APP_DIR"

EOF

output GREEN "Done!"
