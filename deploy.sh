#!/usr/bin/env bash

set -e -u

IMAGES="camera:latest"

APP_DIR="/opt/app"
TMP_DIR="/tmp/$(date +%s)"
PACKAGE="raspberry.img"

function output {
    RED="\033[0;31m"
    GREEN="\033[0;32m"
    YELLOW="\033[1;33m"
    NO_COLOR="\033[0m"
    printf "${!1}${2} ${NO_COLOR}\n"
}

output YELLOW "Building package"
docker-compose build
docker save --output $PACKAGE $IMAGES

output YELLOW "Uploading to Raspberry Pi"
ssh raspi "mkdir $TMP_DIR"
scp -C $PACKAGE docker-compose.yml raspi:$TMP_DIR

output YELLOW "Connecting to Raspberry Pi"
ssh raspi <<EOF
  echo "Creating backups"
  docker save --output "$TMP_DIR"/backup.img "$IMAGES"
  mv "$APP_DIR"/docker-compose.yml "$TMP_DIR"/backup.yml

  echo "Restarting container with new image"
  docker load --input "$TMP_DIR/$PACKAGE"
  mv "$TMP_DIR"/docker-compose.yml "$APP_DIR"/docker-compose.yml
  docker compose -f "$APP_DIR"/docker-compose.yml up -d --force-recreate

  echo "Cleaning up"
  rm -r "$TMP_DIR"

EOF

output GREEN "Done!"
