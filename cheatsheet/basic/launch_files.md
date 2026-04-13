# Launch Files in ROS 2

<details>
<summary>Overview</summary>

- For a package, you create a launch folder in the root directory of the package, and add launch files in it.
- For a global bring up system, you create a separate `bring_up` package. This package does not implement the source code of the nodes, but only launch files. For this tutorial, we will create a `bring_up` package.

</details>

## I. Create a bring_up package with launch files

<details>
<summary> <strong>1. Create a new ROS 2 package</strong></summary>

```bash
cd ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 bring_up
```

</details>

<details>
<summary> <strong>2. Create a <code>launch</code> folder in the root directory of the package and add a launch file </strong></summary>

 _launch.yaml is recommended, but not required, as the file suffix for YAML launch files.

```yaml
# multi_turtle_launch.yaml 
launch:
  - node:
      pkg: "turtlesim"
      exec: "turtlesim_node"
      name: "sim"
      namespace: "turtlesim1"
      args: "--ros-args --log-level info"

  - node:
      pkg: "turtlesim"
      exec: "turtlesim_node"
      name: "sim"
      namespace: "turtlesim2"
      ros_args: "--log-level warn"

  - node:
      pkg: "turtlesim"
      exec: "mimic"
      name: "mimic"
      remap:
        - from: "/input/pose"
          to: "/turtlesim1/turtle1/pose"
        - from: "/output/cmd_vel"
          to: "/turtlesim2/turtle1/cmd_vel"
```


</details>

<details>
<summary> <strong>3. Add dependency on in the <code>package.xml</code></strong></summary>

```xml
<exec_depend>turtlesim</exec_depend>
<exec_depend>ros2launch</exec_depend>
```

</details>

<details>
<summary> <strong>4. Add Launch file paths to <code>setup.py</code> </strong></summary>
In order to use the `ros2 launch` command with the package, we need to include the launch files in the package's data files.

```python
import os
from glob import glob
# Other imports ...

package_name = 'bring_up'

setup(
    # Other parameters ...
    data_files=[
        # ... Other data files
        # Include all launch files.
        (os.path.join('share', package_name, 'launch'), glob('launch/*'))
    ]
)
```


</details>


<details>
<summary> <strong>5. Build the workspace and source the setup file</strong></summary>

```bash
cd ~/ros2_ws
colcon build --packages-select bring_up --symlink-install
source install/setup.bash
```


</details>

<details>
<summary> <strong>6. Run launch file to start the nodes</strong></summary>

```bash
ros2 launch bring_up multi_turtle.yml
```
This will launch two `turtlesim_node` instances in separate namespaces and a `mimic` node that remaps its input and output topics to control the second turtle based on the pose of the first turtle.

you can simply launch the file without building the package by:
```bash
ros2 launch path/to/bring_up/launch/multi_turtle.yml
```
since launch files are just YAML files and do not require compilation. However, if you want to use ROS 2 launch features that depend on the package context (e.g. `FindPackageShare`), then you will need to build the package and source the workspace first.

</details>

## II. Using Substitutions in Launch Files
- Substitutions allow you to reuse the launch files with different parameters or configurations without modifying the default_launch file itself. You can use substitutions to pass arguments, environment variables, or other dynamic values to the nodes being launched.

<details>
<summary>main_launch.yml</summary>  

```yaml
launch:
  - include:
        file: "${find-pkg-share <package_name>}/launch/<default_launch>.yml"
        let:
            - name: "<node_argument>"
              value: "<argument_value>"
```

</details>

<details>
<summary>example of `default_launch.yml`</summary>

```yaml
launch:
  - arg:
        name: "<node_argument>"
        default: "<default_value>"
  - node:
        pkg: "<package_name>"
        exec: "<node_executable>"
        name: "<node_name>"
        args: "--ros-args --param <node_argument>:=<argument_value>"
```