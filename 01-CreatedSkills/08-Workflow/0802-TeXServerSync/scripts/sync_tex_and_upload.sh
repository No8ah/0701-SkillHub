#!/usr/bin/env bash
set -euo pipefail

repo_root="${1:-$(pwd)}"

compile_script="${repo_root}/compile_tex_file.sh"
upload_script="${repo_root}/upload_pdfs_to_server.sh"

if [[ ! -f "${compile_script}" ]]; then
  echo "ERROR: missing script: ${compile_script}" >&2
  exit 1
fi

if [[ ! -f "${upload_script}" ]]; then
  echo "ERROR: missing script: ${upload_script}" >&2
  exit 1
fi

echo "[sync] repo_root=${repo_root}"
echo "[sync] step 1/2: compile tex"
bash "${compile_script}"

echo "[sync] step 2/2: upload pdfs"
bash "${upload_script}"

echo "[sync] done"
