#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${1:-ros2-humble:foxglove}"
CONTAINER_NAME="${CONTAINER_NAME:-ros}"

xhost +localhost
docker run --rm -it \
	--name "${CONTAINER_NAME}" \
	-e DISPLAY="host.docker.internal:0" \
	-e QT_X11_NO_MITSHM=1 \
	"${IMAGE_NAME}" bash