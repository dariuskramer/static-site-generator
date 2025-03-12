#!/usr/bin/env sh

set -o errexit
set -o nounset
set -o xtrace

STATIC_DIR='static'
PUBLIC_DIR='public'

rm --verbose --preserve-root --recursive "${PUBLIC_DIR}"
mkdir --verbose "${PUBLIC_DIR}"
cp --verbose --recursive "${STATIC_DIR}"/* "${PUBLIC_DIR}/"

python src/main.py
cd public && python -m http.server 8888
