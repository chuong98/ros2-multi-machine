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
- This can be done with the package `ros2 run tf2_ros static_transform_publisher`, but we will write our own static transform broadcaster node using the class `tf2_ros.static_transform_broadcaster.StaticTransformBroadcaster`.

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
<summary>Step 5: Build the package and run the static transform broadcaster node</summary> w

```bash
rosdep install -i --from-path src --rosdistro jazzy -y
colcon build --packages-select my_tf2 --symlink-install
```

</details>

## 4. Write Dynamic Transform Broadcaster
- The dynamic transform broadcaster is used to publish a transformation that changes over time.
- [turtle_tf2_broadcaster.py](../../src/my_tf2/my_tf2/turtle_tf2_broadcaster.py)  use the class `tf2_ros.TransformBroadcaster` that subscribes to the turtle's pose and publishes the transformation between the world frame and the turtle frame.
- [turtle_tf2_listener.py](../../src/my_tf2/my_tf2/turtle_tf2_listener.py) use the class `tf2_ros.TransformListener` to listen to all the transformations and write to the buffer `tf2_ros.Buffer`. Then it uses the function `Buffer.lookup_transform()`, to get the coordinate of `turtle1` w.r.t `turtle2`, then compute the cmd speed to track `turtle1`.
- Write a launch file to start the turtlesim nodes:
    - run 2 dynamic transform broadcaster nodes for `turtle1` and `turtle2` to broadcast their coordinate in the world frame.
    - the listener node spawns a new turtle in the turtlesim, then compute the command to drive `turtle2` to follow `turtle1`.
- run the demo:
`ros2 launch learning_tf2_py turtle_tf2_demo_launch.xml`

## 5. Adding Frame to the TF Tree
- In many cases, you may want to add a new frame to the TF tree to represent a new coordinate system in your robot or environment. It could be a sensor frame, an end-effector frame, or any other frame that is relevant to your application.
- To add a new frame to the TF tree, you can create a new transform broadcaster node that publishes the transformation between the new frame and an existing frame in the TF tree. 
- [carrot_tf2_brodcaster.py](../../src/my_tf2/my_tf2/carrot_tf2_broadcaster.py) creates a frame `carrot` relative to `turtle1` and let the `turtle2` track the `carrot`. 

## 6. TF2_ROS::MessageFilter and PointStamp
- Imaging that there is `turtle3` that does not have odometry, but there is GPS that can track and publish its position. `turtle1` wants to know where `turtle3` is compared to itself.
- To do this `turtle1` must listen to the topic where `turtle3’s pose` is being published, wait until transforms into the desired frame are ready, and then do its operations. To make this easier the `tf2_ros::MessageFilter` is very useful. It will take a subscription to any ROS 2 message with a header and cache it until it is possible to transform it into the target frame.
- Use `tf2:PointStamped` to publish a point coordinate in a coordinate (local or global).