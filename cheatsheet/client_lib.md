# Build ROS Package and Inspect Rosdep

## Build Package
run `colcon build` in the root of your workspace to build all packages. After building, there are 4 folders in the root of your workspace:
- `build/`: Contains build files for each package.
- `install/`: Contains installed files for each package. This is where you source to use the packages in your workspace.
- `log/`: Contains build logs.
- `src/`: Contains source code for your packages.

| Syntax | Explanation | Example |
| --- | --- | --- |
| `colcon build --packages-select <package_name>` | Build one package only. | `colcon build --packages-select my_robot_pkg` |
| `colcon build --symlink-install` | Build all packages with symlink install (good for development). | `colcon build --symlink-install` |
| `source install/setup.bash` | Source built workspace so packages are discoverable. | `source install/setup.bash` |
| `ros2 pkg create --build-type ament_python/ament_cmake --license Apache-2.0 <package_name>` | Create a new ROS package with Python/C++ build type. This must run at `src` folder. | `ros2 pkg create --build-type ament_python --license Apache-2.0 my_robot_pkg` |


## Inspect Rosdep

| Syntax | Explanation | Example |
| --- | --- | --- |
| `rosdep --version` | Check installed `rosdep` version. | `rosdep --version` |
| `rosdep db` | Print the current rosdep database summary. | `rosdep db` |
| `rosdep keys <path_to_package_or_src>` | List dependency keys declared in package manifests. | `rosdep keys src/my_robot_pkg` |
| `rosdep check --from-paths src --ignore-src -r -y` | Check whether required system dependencies are installed. | `rosdep check --from-paths src --ignore-src -r -y` |
| `rosdep resolve <key>` | Show how a rosdep key maps to OS packages. | `rosdep resolve rclcpp` |
| `rosdep install --from-paths src --ignore-src -r -y` | Install missing system dependencies for all packages in `src/`. | `rosdep install --from-paths src --ignore-src -r -y` |


