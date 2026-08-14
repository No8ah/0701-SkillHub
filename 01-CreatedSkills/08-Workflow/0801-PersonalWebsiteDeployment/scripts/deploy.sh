#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/Users/quzinan/Downloads/Code/personal_website_react}"
REMOTE_HOST="${REMOTE_HOST:-8.134.74.103}"
REMOTE_USER="${REMOTE_USER:-root}"
REMOTE_DIR="${REMOTE_DIR:-/var/www/html}"
REMOTE_TMP="${REMOTE_TMP:-/tmp/personal-website-dist.tar.gz}"
export REMOTE_HOST REMOTE_USER

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'ERROR: required command not found: %s\n' "$1" >&2
    exit 1
  fi
}

shell_quote() {
  printf "'%s'" "$(printf '%s' "$1" | sed "s/'/'\\\\''/g")"
}

run_ssh() {
  local remote_command="$1"
  if [[ -n "${DEPLOY_PASSWORD:-}" ]]; then
    REMOTE_COMMAND="$remote_command" expect <<'EOF'
log_user 0
set timeout 60
spawn ssh -o StrictHostKeyChecking=accept-new -o PubkeyAuthentication=no "$env(REMOTE_USER)@$env(REMOTE_HOST)" "$env(REMOTE_COMMAND)"
expect {
  -re "(?i)password:" { log_user 0; send "$env(DEPLOY_PASSWORD)\r"; log_user 1; exp_continue }
  eof
}
catch wait result
exit [lindex $result 3]
EOF
  else
    ssh -o StrictHostKeyChecking=accept-new "${REMOTE_USER}@${REMOTE_HOST}" "$remote_command"
  fi
}

run_scp() {
  local src="$1"
  local dst="$2"
  if [[ -n "${DEPLOY_PASSWORD:-}" ]]; then
    SCP_SRC="$src" SCP_DST="$dst" expect <<'EOF'
log_user 0
set timeout 60
spawn scp -o StrictHostKeyChecking=accept-new -o PubkeyAuthentication=no "$env(SCP_SRC)" "$env(SCP_DST)"
expect {
  -re "(?i)password:" { send "$env(DEPLOY_PASSWORD)\r"; exp_continue }
  eof
}
catch wait result
exit [lindex $result 3]
EOF
  else
    scp -o StrictHostKeyChecking=accept-new "$src" "$dst"
  fi
}

require_cmd npm
require_cmd tar
require_cmd ssh
require_cmd scp
if [[ -n "${DEPLOY_PASSWORD:-}" ]]; then
  require_cmd expect
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
  printf 'ERROR: project directory does not exist: %s\n' "$PROJECT_DIR" >&2
  exit 1
fi

log "Building $PROJECT_DIR"
(cd "$PROJECT_DIR" && npm run build)

DIST_DIR="$PROJECT_DIR/dist"
if [[ ! -f "$DIST_DIR/index.html" ]]; then
  printf 'ERROR: build did not produce %s\n' "$DIST_DIR/index.html" >&2
  exit 1
fi

ARCHIVE="$(mktemp -t personal-website-dist.XXXXXX.tar.gz)"
trap 'rm -f "$ARCHIVE"' EXIT

log "Packaging dist"
COPYFILE_DISABLE=1 tar -C "$DIST_DIR" --exclude='._*' -czf "$ARCHIVE" .

log "Uploading archive to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_TMP}"
run_scp "$ARCHIVE" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_TMP}"

quoted_remote_dir="$(shell_quote "$REMOTE_DIR")"
quoted_remote_tmp="$(shell_quote "$REMOTE_TMP")"
remote_command="mkdir -p $quoted_remote_dir && rm -rf $quoted_remote_dir/assets $quoted_remote_dir/index.html $quoted_remote_dir/resume.pdf && tar -xzf $quoted_remote_tmp -C $quoted_remote_dir && rm -f $quoted_remote_tmp && find $quoted_remote_dir -name '._*' -delete && chown -R root:root $quoted_remote_dir && find $quoted_remote_dir -type f -exec chmod 644 {} +"

log "Publishing to ${REMOTE_DIR}"
run_ssh "$remote_command"

log "Verifying checksums"
local_sums="$(cd "$DIST_DIR" && sha256sum index.html assets/*.js assets/*.css resume.pdf | sort | tr -d '\r' | sed '/^$/d')"
remote_sums="$(run_ssh "cd $quoted_remote_dir && sha256sum index.html assets/*.js assets/*.css resume.pdf | sort" | tr -d '\r' | sed '/^$/d')"

if [[ "$local_sums" != "$remote_sums" ]]; then
  printf 'ERROR: checksum verification failed\n\nLocal:\n%s\n\nRemote:\n%s\n' "$local_sums" "$remote_sums" >&2
  exit 1
fi

log "Deployment verified: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"
