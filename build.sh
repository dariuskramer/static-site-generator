#!/usr/bin/env sh

set -o errexit
set -o nounset
set -o xtrace

STATIC_DIR='static'
DEPLOY_DIR='docs'
REPO_NAME='/static-site-generator/'

rm --verbose --force --preserve-root --recursive "${DEPLOY_DIR}"
mkdir --verbose "${DEPLOY_DIR}"
cp --verbose --recursive "${STATIC_DIR}"/* "${DEPLOY_DIR}/"

python src/main.py "${DEPLOY_DIR}" "${REPO_NAME}"
cd "${DEPLOY_DIR}" && python -m http.server 8888
