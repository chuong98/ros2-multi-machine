# Basic ROS2 CLI Commands

## General

| Syntax | Explanation | Example |
| --- | --- | --- |
| `echo $ROS_DISTRO` | Show the installed ROS2 distribution. | `echo $ROS_DISTRO` |
| `ros2 doctor` | Check the health of your ROS2 installation and environment. | `ros2 doctor` |
| `colcon build` | Build packages in the current ROS2 workspace. | `colcon build --symlink-install` |
| `source install/setup.bash` | Source the workspace so built packages are available in the shell. | `source install/setup.bash` |

## Package

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 pkg list` | List all available ROS2 packages in the environment. | `ros2 pkg list` |
| `ros2 pkg create <package_name> --build-type ament_python --license <license_name>` | Create a new ROS2 package. | `ros2 pkg create my_robot_pkg --build-type ament_python --license Apache-2.0` |
| `ros2 pkg executables <package_name>` | List executables provided by a package. | `ros2 pkg executables turtlesim` |

## Node

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 run <package_name> <executable_name>` | Run a node from a package. | `ros2 run turtlesim turtlesim_node` |
| `ros2 node list` | List currently running nodes. | `ros2 node list` |
| `ros2 node info <node_name>` | Show publishers, subscribers, services, and actions for a node. | `ros2 node info /turtlesim` |

## Launch

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 launch <package_name> <launch_file>` | Launch one or more nodes from a launch file. | `ros2 launch foxglove_bridge foxglove_bridge_launch.xml` |
| `ros2 launch <package_name> <launch_file> --show-args` | Show available launch arguments for a launch file. | `ros2 launch py_package fibonacci_action.launch.py --show-args` |
| `ros2 launch <package_name> <launch_file> <arg_name>:=<value>` | Pass launch arguments from the command line. | `ros2 launch turtlesim multisim.launch.py use_sim_time:=true` |
| `ros2 launch <package_name> <launch_file> --debug` | Run launch with debug logging to troubleshoot startup issues. | `ros2 launch py_package fibonacci_action.launch.py --debug` |


## Topic
- One node publishes messages to a topic, and other nodes subscribe to that topic to receive the messages. 
- Topics are used for unidirectional, asynchronous communication between nodes.
  

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 topic list` | List active topics. | `ros2 topic list` |
| `ros2 topic echo <topic_name>` | Print messages being published on a topic. | `ros2 topic echo /turtle1/pose` |
| `ros2 topic pub <topic_name> <msg_type> <data>` | Publish a message to a topic from the CLI. | `ros2 topic pub /chatter std_msgs/msg/String "{data: 'hello'}"` |
| `ros2 topic info <topic_name>` | Show publishers, subscribers, and type information for a topic. | `ros2 topic info /turtle1/cmd_vel` |
| `ros2 topic hz <topic_name>` | Measure how fast messages are being published on a topic. | `ros2 topic hz /turtle1/pose` |

- Record, publish topic by `yml` file 

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 topic echo --once <topic_name> > <yaml_file.yml>` | Save a message published on a topic to a YAML file. | `ros2 topic echo --once /turtle1/pose > pose.yaml` |
| `ros2 topic pub <topic_name> <msg_type> --yaml-file <yaml_file.yml>` | Publish messages to a topic from a YAML file. | `ros2 topic pub /turtle1/pose geometry_msgs/msg/Pose --yaml-file pose.yaml` |

## Service
- A service consists of a request and a response. One node offers a service, and other nodes can call that service to send a request and receive a response. 
- It is often for instantaneous interactions, such as requesting data or triggering an action, where the caller needs a response before proceeding.

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 service list` | List available services. | `ros2 service list` |
| `ros2 service type <service_name>` | Show the service type for a service name. | `ros2 service type /clear` |
| `ros2 service call <service_name> <service_type> <request>` | Call a service from the CLI. | `ros2 service call /clear std_srvs/srv/Empty "{}"` |

## Action
- An action consists of a goal, feedback, and a result. One node acts as an action server that executes the task, while other nodes can act as action clients that send goals to the server and receive feedback and results.
- Actions are ideal for long-running tasks, such as moving a robot to a location or performing a complex computation, where the client receives updates on the progress and can cancel the task if needed.

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 action list` | List available action servers and clients. | `ros2 action list` |
| `ros2 action info <action_name>` | Show the action type and connected endpoints. | `ros2 action info /fibonacci` |
| `ros2 action send_goal <action_name> <action_type> <goal>` | Send a goal to an action server from the CLI. | `ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 10}"` |

## Interface of Message, Service, Action
- ROS2 interfaces define the structure of messages, services, and actions that nodes use to communicate. 
- They are defined in `.msg`, `.srv`, and `.action` files.

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 interface list` | List all available message, service, and action interfaces. | `ros2 interface list` |
| `ros2 interface package <package_name>` | List all available message, service, and action interfaces in a specific package. | `ros2 interface package example_interfaces` |
| `ros2 interface show <interface_type>` | Show the definition of a message, service, or action type. | `ros2 interface show geometry_msgs/msg/Twist` |


## Parameters
- Parameters are node-level configuration values that can be read and updated at runtime.

| Syntax | Explanation | Example |
| --- | --- | --- |
| `ros2 param list` | List parameters available on running nodes. | `ros2 param list` |
| `ros2 param get <node_name> <parameter_name>` | Get the current value of a parameter. | `ros2 param get /minimal_param_node my_param` |
| `ros2 param set <node_name> <parameter_name> <value>` | Set a parameter value on a running node. | `ros2 param set /minimal_param_node my_param earth` |
| `ros2 param describe <node_name> <parameter_name>` | Show type and descriptor info for a parameter. | `ros2 param describe /minimal_param_node my_param` |
| `ros2 param dump <node_name>` | Export a node's parameters to YAML. | `ros2 param dump /minimal_param_node` |
| `ros2 param load <node_name> <yaml_file>` | Load parameters from a YAML file into a running node. | `ros2 param load /minimal_param_node params.yaml` |