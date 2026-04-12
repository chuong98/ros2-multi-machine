#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${1:-ros2-humble:foxglove}"
CONTAINER_NAME="${CONTAINER_NAME:-ros-humble}"

xhost +localhost
docker run --rm -it -d \
	--name "${CONTAINER_NAME}" \
	-e DISPLAY="host.docker.internal:0" \
	-e QT_X11_NO_MITSHM=1 \
	-v ./ros2_ws:/home/chuongnguyen/ros2_ws \
	-v ../cheatsheet:/home/chuongnguyen/ros2_ws/cheatsheet \
	-w /home/chuongnguyen/ros2_ws \
	"${IMAGE_NAME}" bash