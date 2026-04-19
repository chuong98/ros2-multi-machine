#!/bin/bash
set -e

source /opt/ros/humble/setup.bash

echo "Starting turtlesim node..."
ros2 run turtlesim turtlesim_node            
