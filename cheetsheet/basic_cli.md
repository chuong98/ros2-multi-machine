# Basic ROS2 CLI Commands

## General

| Syntax | Explainatin | Example |
| --- | --- | --- |
| `ros2 --version` | Show the installed ROS2 CLI version. | `ros2 --version` |
| `ros2 launch <package_name> <launch_file>` | Start one or more nodes from a launch file. | `ros2 launch turtlesim multisim.launch.py` |

## Package

| Syntax | Explainatin | Example |
| --- | --- | --- |
| `ros2 pkg list` | List all available ROS2 packages in the environment. | `ros2 pkg list` |
| `ros2 pkg create <package_name> --build-type ament_python` | Create a new ROS2 package. | `ros2 pkg create my_robot_pkg --build-type ament_python` |
| `ros2 pkg executables <package_name>` | List executables provided by a package. | `ros2 pkg executables turtlesim` |

## Node

| Syntax | Explainatin | Example |
| --- | --- | --- |
| `ros2 run <package_name> <executable_name>` | Run a node from a package. | `ros2 run turtlesim turtlesim_node` |
| `ros2 node list` | List currently running nodes. | `ros2 node list` |
| `ros2 node info <node_name>` | Show publishers, subscribers, services, and actions for a node. | `ros2 node info /turtlesim` |

## Topic
- One node publishes messages to a topic, and other nodes subscribe to that topic to receive the messages. 
- Topics are used for unidirectional, asynchronous communication between nodes.
  

| Syntax | Explainatin | Example |
| --- | --- | --- |
| `ros2 topic list` | List active topics. | `ros2 topic list` |
| `ros2 topic echo <topic_name>` | Print messages being published on a topic. | `ros2 topic echo /turtle1/pose` |
| `ros2 topic pub <topic_name> <msg_type> <data>` | Publish a message to a topic from the CLI. | `ros2 topic pub /chatter std_msgs/msg/String "{data: 'hello'}"` |
| `ros2 topic info <topic_name>` | Show publishers, subscribers, and type information for a topic. | `ros2 topic info /turtle1/cmd_vel` |
| `ros2 topic hz <topic_name>` | Measure how fast messages are being published on a topic. | `ros2 topic hz /turtle1/pose` |

## Service
- Two nodes can communicate synchronously using services. A service consists of a request and a response. One node offers a service, and other nodes can call that service to send a request and receive a response. 
- It is often for instantaneous interactions, such as requesting data or triggering an action, where the caller needs a response before proceeding.
  

| Syntax | Explainatin | Example |
| --- | --- | --- |
| `ros2 service list` | List available services. | `ros2 service list` |
| `ros2 service type <service_name>` | Show the service type for a service name. | `ros2 service type /clear` |
| `ros2 service call <service_name> <service_type> <request>` | Call a service from the CLI. | `ros2 service call /clear std_srvs/srv/Empty "{}"` |

## Action
- Actions are used for long-running tasks that can provide feedback and be preempted. An action consists of a goal, feedback, and a result. One node acts as an action server that executes the task, while other nodes can act as action clients that send goals to the server and receive feedback and results.
- Actions are ideal for tasks that may take some time to complete, such as moving a robot to a location or performing a complex computation, where the client may want to receive updates on the progress and have the ability to cancel the task if needed.
- Action can be canceled by the client, allowing for more flexible and responsive interactions between nodes. This is particularly useful in scenarios where the task may take an unpredictable amount of time or when the client needs to change its goals based on new information.

| Syntax | Explainatin | Example |
| --- | --- | --- |
| `ros2 action list` | List available action servers and clients. | `ros2 action list` |
| `ros2 action info <action_name>` | Show the action type and connected endpoints. | `ros2 action info /fibonacci` |
| `ros2 action send_goal <action_name> <action_type> <goal>` | Send a goal to an action server from the CLI. | `ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 10}"` |

## Interface

| Syntax | Explainatin | Example |
| --- | --- | --- |
| `ros2 interface list` | List all available message, service, and action interfaces. | `ros2 interface list` |
| `ros2 interface show <interface_type>` | Show the definition of a message, service, or action type. | `ros2 interface show geometry_msgs/msg/Twist` |

## Workspace

| Syntax | Explainatin | Example |
| --- | --- | --- |
| `colcon build` | Build packages in the current ROS2 workspace. | `colcon build --symlink-install` |
| `source install/setup.bash` | Source the workspace so built packages are available in the shell. | `source install/setup.bash` |