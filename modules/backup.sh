#!/usr/bin/env bash

set -e
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'

BACKUP_DIR="./backups"
NGINX_DIR="/etc/nginx"
WEB_DIR="/var/www/html"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M")
BACKUP_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"

printf "${CYAN}[START] Creating backup...${RESET}\n"

tar -czf "$BACKUP_FILE" \
    -C / \
    "${NGINX_DIR#/}" \
    "${WEB_DIR#/}"

printf "${BLUE}[DONE] Backup is ready: $BACKUP_FILE ${RESET}\n"

printf "${YELLOW}[INFO] Cleaning backups older than 3 days...${RESET}\n"

printf "${RED}\n"
find "$BACKUP_DIR" \
    -type f \
    -name "backup_*.tar.gz" \
    -mtime +3 \
    -print \
    -delete
printf "${RESET}\n"

printf "${GREEN}[OK] Cleanup done.${RESET}\n\n"


