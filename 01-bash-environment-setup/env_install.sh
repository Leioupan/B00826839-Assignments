#!/usr/bin/env bash
# Provision Python 3, pip, and Jupyter on macOS or Debian/Ubuntu Linux.
set -Eeuo pipefail

DRY_RUN=false
VERBOSE=false
QUIET=false
LOG_FILE="${LOG_FILE:-env_install.log}"
JUPYTER_VENV="${JUPYTER_VENV:-$HOME/.local/share/jupyter-venv}"

usage() {
  cat <<'USAGE'
Usage: ./env_install.sh [--dry-run] [--verbose] [--quiet]

Installs Python 3 and Jupyter in an isolated virtual environment.
On macOS, runs `brew doctor` after installation.
USAGE
}

log() {
  local level="$1"; shift
  local message="$*"
  printf '%s [%s] %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$level" "$message" >> "$LOG_FILE"
  if [[ "$QUIET" != true || "$level" == ERROR ]]; then
    case "$level" in
      SUCCESS) printf '\033[32m%s\033[0m\n' "$message" ;;
      WARN) printf '\033[33m%s\033[0m\n' "$message" ;;
      ERROR) printf '\033[31m%s\033[0m\n' "$message" >&2 ;;
      *) printf '%s\n' "$message" ;;
    esac
  fi
}

run() {
  if [[ "$DRY_RUN" == true ]]; then
    log INFO "[dry-run] $*"
  else
    [[ "$VERBOSE" == true ]] && log INFO "Running: $*"
    "$@"
  fi
}

trap 'status=$?; log ERROR "Command failed (exit $status) at line $LINENO"; exit "$status"' ERR

while (($#)); do
  case "$1" in
    --dry-run) DRY_RUN=true ;;
    --verbose|-v) VERBOSE=true ;;
    --quiet|-q) QUIET=true ;;
    --help|-h) usage; exit 0 ;;
    *) log ERROR "Unknown option: $1"; usage >&2; exit 2 ;;
  esac
  shift
done

pretty_print() { printf '\n%s\n\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

install_linux() {
  [[ -x /usr/bin/apt-get ]] || { log ERROR "This Linux installer supports Debian/Ubuntu (apt-get) only."; return 1; }
  if ! have python3; then
    log INFO "Installing Python 3 with apt-get."
    run sudo apt-get update
    run sudo apt-get install -y python3
  else
    log SUCCESS "Python 3 already installed: $(python3 --version)"
  fi
  run sudo apt-get update
  run sudo apt-get install -y python3-venv
  run python3 -m venv "$JUPYTER_VENV"
  run "$JUPYTER_VENV/bin/python" -m pip install --upgrade pip
  run "$JUPYTER_VENV/bin/python" -m pip install notebook
}

install_macos() {
  have brew || { log ERROR "Homebrew is required on macOS. Install it from https://brew.sh/ and retry."; return 1; }
  if ! have python3; then run brew install python; else log SUCCESS "Python 3 already installed: $(python3 --version)"; fi
  run python3 -m venv "$JUPYTER_VENV"
  run "$JUPYTER_VENV/bin/python" -m pip install --upgrade pip
  run "$JUPYTER_VENV/bin/python" -m pip install notebook
  log INFO "Checking Homebrew health."
  run brew doctor
}

pretty_print "Starting development environment setup"
log INFO "Detected OSTYPE=${OSTYPE:-unknown}"
case "${OSTYPE:-}" in
  darwin*) install_macos ;;
  linux*) install_linux ;;
  *) log ERROR "Unsupported operating system: ${OSTYPE:-unknown}"; exit 1 ;;
esac

if [[ "$DRY_RUN" != true ]]; then
  "$JUPYTER_VENV/bin/python" -m pip --version
  log SUCCESS "Python, pip, and Jupyter setup is complete. Start Jupyter with: $JUPYTER_VENV/bin/jupyter notebook"
else
  log SUCCESS "Dry run complete; no changes were made."
fi
