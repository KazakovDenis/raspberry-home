#!/usr/bin/env sh

set -eu
echo "$(date)"

BACKUP_SOURCE_DIR=/media/share
IGNORE_FILE=ignore.txt

BACKUP_SECRET_SRC="private"
BACKUP_SECRET_DST=secret:

BACKUP_OPEN_SRC="public"
BACKUP_OPEN_DST=remote:backup

LOG_FILE=/var/log/rclone-backup.log
LOG_LEVEL=INFO

for i in $BACKUP_SECRET_SRC; do
  echo "Synchronizing $i..."
  rclone --log-file $LOG_FILE --log-level $LOG_LEVEL sync --exclude-from $IGNORE_FILE --progress $BACKUP_SOURCE_DIR/$i $BACKUP_SECRET_DST/$i
done

for i in $BACKUP_OPEN_SRC; do
  echo "Synchronizing $i..."
  rclone --log-file $LOG_FILE --log-level $LOG_LEVEL sync --exclude-from $IGNORE_FILE --progress $BACKUP_SOURCE_DIR/$i $BACKUP_OPEN_DST/$i
done

echo "Done!"
