# Learn ROS TF2 library

## 1. Setup
- This demo is using the tf2 library to create three coordinate frames: a world frame, a turtle1 frame, and a turtle2 frame. This tutorial uses a tf2 broadcaster to publish the turtle coordinate frames and a tf2 listener to compute the difference in the turtle frames and move one turtle to follow the other.

```bash
sudo apt-get install ros-jazzy-rviz2 ros-jazzy-turtle-tf2-py ros-jazzy-tf2-ros ros-jazzy-tf2-tools ros-jazzy-turtlesim
ros2 launch turtle_tf2_py turtle_tf2_demo.launch.py # run the demo
ros2 run turtlesim turtle_teleop_key # in the second terminal, control the turtle with the keyboard
```

# 2. Visualize
- Run foxglove to visualize the coordinate frames and the movement of the turtles.

```bash
ros2 run foxglove_bridge foxglove_bridge --ros-bridge-url ws://localhost:9090
```
- Open the Foxglove Studio and add a "Transform Tree" panel to visualize the coordinate frames. You should see the world frame, turtle1 frame, and turtle2 frame. As you move turtle1 with the keyboard, you should see turtle2 following it, demonstrating the use of tf2 for coordinate transformations.