#!/bin/sh
CURRENT_DIR="$(cd "$(dirname "${0}")" && pwd)"

set -x

cd "${CURRENT_DIR}"
SECS="3"
while :; do docker-compose build && docker-compose up; echo "respawing in ${SECS} secs ..."; sleep "${SECS}"; done
