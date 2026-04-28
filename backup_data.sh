#!/bin/bash
# Backup ClimateGuard Database
TIMESTAMP=$(date +"%F")
BACKUP_DIR="../backups"

mkdir -p $BACKUP_DIR
pg_dump climateguard_db > $BACKUP_DIR/backup_$TIMESTAMP.sql

echo "ClimateGuard Backup completed for $TIMESTAMP"
