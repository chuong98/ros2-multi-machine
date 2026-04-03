#!/bin/bash
set -e

source /opt/ros/humble/setup.bash

echo "Starting teleop node..."
ros2 run turtlesim turtle_teleop_key