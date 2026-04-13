# Learn ROS TF2 library

## 1. Setup
- This demo is using the tf2 library to create three coordinate frames: a world frame, a turtle1 frame, and a turtle2 frame. 
- This tutorial uses a tf2 broadcaster to publish the turtle coordinate frames and a tf2 listener to compute the difference in the turtle frames and move one turtle to follow the other.

```bash
sudo apt-get update
sudo apt-get install ros-jazzy-turtle-tf2-py ros-jazzy-tf2-ros ros-jazzy-tf2-tools ros-jazzy-turtlesim
ros2 launch turtle_tf2_py turtle_tf2_demo.launch.py # run the demo
ros2 run turtlesim turtle_teleop_key # in the second terminal, control the turtle with the keyboard
```

## 2. Visualize
- Run foxglove to visualize the coordinate frames and the movement of the turtles.

```bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml 
```
Add the panels: 
  - "Transform Tree" to visualize the coordinate frames and their relationships.
  - "Topic Graph" to see the communication between nodes and topics.
  - "3D View" to visualize the turtles and their movements in a 3D space.

## 3. Write static transform broadcaster
- The static transform broadcaster is used to publish a fixed transformation between two coordinate frames. 
- This can be done with the package `ros2 run tf2_ros static_transform_publisher`, but we will write our own static transform broadcaster node to understand how it works.

The steps are similar to general [ROS2 package development](../basic/ros_package.md). 

<details>
<summary>Step 2: Create a my_tf2 package and add static_tf_broadcaster.py</summary>

Create a `my_tf2` package and add a [`static_tf_broadcaster.py`](../../src/my_tf2/my_tf2/static_tf2_broadcaster.py) file in the `my_tf2/my_tf2` folder.

</details>

<details>
<summary>Step 3: Add the dependency in the package.xml file</summary>

```yaml
<exec_depend>geometry_msgs</exec_depend>
<exec_depend>python3-numpy</exec_depend>
<exec_depend>rclpy</exec_depend>
<exec_depend>tf2_ros_py</exec_depend>
<exec_depend>turtlesim</exec_depend>
```

</details>

<details>
<summary>Step 4: Add static_tf_broadcaster.py to the setup.py file</summary>

```python
entry_points={
    'console_scripts': [
        'static_tf_broadcaster = my_tf2.static_tf_broadcaster:main',
    ],
},
```

</details>

<details>
<summary>Step 5: Build the package and run the static transform broadcaster node</summary>

```bash
rosdep install -i --from-path src --rosdistro jazzy -y
colcon build --packages-select my_tf2 --symlink-install
```

</details>