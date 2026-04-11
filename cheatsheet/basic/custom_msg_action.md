
# Custome Interfaces in ROS 2
- Custom messages and services allow you to define your own data structures for communication between nodes.
- They are defined in `.msg` and `.srv` files within a ROS 2 C++ package, and then built to generate code for use in any other packages (python/C++).

##  I. Create a custom message package
<details>
<summary><strong>Step 1. Create a new package for custom messages</strong></summary>

```bash
cd ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 msg_package
```
Note:
- it can only be an `ament_cmake` package
- You can create custom messages and services in the same package, but it is often better to separate them. It avoids unnecessary dependencies, circular dependencies problems, and makes it easier to reuse the message package across different projects. 

</details>

<details>
<summary><strong>Step 2. Create a custom message/service definition</strong></summary>

<details>
<summary>msg_package/msg/Sphere.msg</summary>

```bash
geometry_msgs/Point center
float64 radius
```

</details>

<details>
<summary>msg_package/srv/CheckSphereOverlap.srv</summary>

```bash
msg_package/Sphere a
msg_package/Sphere b
---
bool overlap
```

</details>

</details>

<details>
<summary><strong>Step 3. Update <code>CMakeLists.txt</code> to build messages and services</strong></summary>

```cmake
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Sphere.msg"
  "srv/CheckSphereOverlap.srv"
  DEPENDENCIES geometry_msgs
)
```

</details>

<details>
<summary><strong>Step 4. Add dependencies to <code>package.xml</code></strong></summary>

- Add `geometry_msgs` as a runtime dependency
- Add `rosidl_default_generators` and `rosidl_default_runtime` as build and exec dependencies for message generation. 
- Add the package to the `rosidl_interface_packages` group.
```xml
<depend>geometry_msgs</depend>
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

</details>

<details>
<summary><strong>Step 5. Build the package and source the workspace</strong></summary>

```bash
cd ~/ros2_ws
colcon build --packages-select msg_package
source install/setup.bash
```
Check that the generated message and service Python modules are available:
```bash
ros2 interface show msg_package/msg/Sphere
ros2 interface show msg_package/srv/CheckSphereOverlap
```

</details>


## II. Create a custom action package
All the steps are similar to the custom message package, except:
- Step 2: you create an action definition in a `.action` file.
- Step 3: the dependencies in `CMakeLists.txt` also include `action_msgs` for the action interfaces.
- Step 4: the dependencies in `package.xml` also include `action_msgs` for the action interfaces.
### Step 2. Create a custom action definition in `action/`:
<details>
<summary>msg_package/action/MoveRobot.action</summary>

```bash
# Goal
geometry_msgs/Point target
float64 speed
---
# Result
bool success
---
# Feedback
float64 distance_remaining
```

### Step 3. Update `CMakeLists.txt` to build the action interface:
```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/Fibonacci.action"
)
```

### Step 4. Add dependencies to `package.xml`:
```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<depend>action_msgs</depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```