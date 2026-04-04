#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

detect_platform() {
    local os
    os="$(uname -s)"

    if [[ "$os" == "Darwin" ]]; then
        echo "local"
        xhost +localhost
        return
    fi

    if [[ "$os" == "Linux" ]]; then
        # Jetson devices expose their model in /proc/device-tree/model
        if [[ -f /proc/device-tree/model ]] && grep -qi "jetson" /proc/device-tree/model 2>/dev/null; then
            echo "jetson"
        else
            echo "remote"
        fi
        return
    fi

    echo "Unsupported platform: $os" >&2
    exit 1
}

PLATFORM="$(detect_platform)"
echo "Detected platform: $PLATFORM"

cd "$SCRIPT_DIR/$PLATFORM"
docker compose up "$@"
