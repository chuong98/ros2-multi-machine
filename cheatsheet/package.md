# Minimal Package Example in ROS 2 with Python

## I. Publisher-Subscriber Example
### 1. Create a package with Python build type:
```bash
cd ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 py_package	--dependencies rclpy
```

### 2. Create publisher and subscriber nodes in `src/py_package/`:

<details>
<summary>publisher_node.py</summary>

```python
# publisher_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PublisherNode(Node):
	def __init__(self):
		super().__init__('publisher_node')
		self.publisher_ = self.create_publisher(String, 'topic', 10)
		timer_period = 1.0  # seconds
		self.timer = self.create_timer(timer_period, self.timer_callback)

	def timer_callback(self):
		msg = String()
		msg.data = 'Hello, ROS 2!'
		self.publisher_.publish(msg)
		self.get_logger().info(f'Publishing: "{msg.data}"')	

def main(args=None):
	rclpy.init(args=args)
	publisher_node = PublisherNode()
	rclpy.spin(publisher_node)
	publisher_node.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()
```

</details>

<details>
<summary>subscriber_node.py</summary>

```python
# subscriber_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SubscriberNode(Node):
	def __init__(self):
		super().__init__('subscriber_node')
		self.subscription = self.create_subscription( String, 'topic', self.listener_callback, 10)
		self.subscription  # prevent unused variable warning

	def listener_callback(self, msg):
		self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
	rclpy.init(args=args)
	subscriber_node = SubscriberNode()
	rclpy.spin(subscriber_node)
	subscriber_node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()	
```

</details>

### 3. Add dependencies to `package.xml`:
```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>std_msgs</exec_depend>
```
### 4. Add console scripts to `setup.py`:
```python
entry_points={
	'console_scripts': [
		# executable_name = package_name.module_name:function_name
		'talker = py_package.publisher_node:main',
		'listener = py_package.subscriber_node:main',
	],
},
```
### 5. Build the package and source the workspace:
```bash
cd ~/ros2_ws
colcon build --packages-select py_package --symlink-install
source install/setup.bash
```
After build and source, you can run the nodes from the CLI:
```bash
ros2 pkg executables py_package
```
you should see `talker` and `listener` in the output. 

## II. Service-Client Example
All the steps are similar to the publisher-subscriber example, except: 
-	Step 2: you create service and client nodes. 
-	Step 3: the dependencies in `package.xml` also include `example_interfaces` for the service interface. 
-	Step 4: the console scripts in `setup.py` will be updated to point to the new service and client nodes.

### Step  2. Create service and client nodes in `src/py_package/`:

<details>
<summary>service_node.py</summary>

```python
# service_node.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts		
class ServiceNode(Node):
	def __init__(self):
		super().__init__('service_node')
		self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.service_callback)

	def service_callback(self, request, response):
		response.sum = request.a + request.b
		self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}, sum={response.sum}')
		return response
def main(args=None):
	rclpy.init(args=args)
	service_node = ServiceNode()
	rclpy.spin(service_node)
	service_node.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()
```

</details>

<details>
<summary>client_node.py</summary>

```python
# client_node.py
import rclpy
import sys
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalClient(Node):
    def __init__(self):
        super().__init__('minimal_client')
        self.client_ = self.create_client(AddTwoInts,'add_ints')
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
        self.request_ = AddTwoInts.Request()

    def send_request(self, a, b):
        self.request_.a = a
        self.request_.b = b
        return self.client_.call_async(self.request_)   
    
def main():
    rclpy.init()
    client  = MinimalClient()
    future = client.send_request(int(sys.argv[1]),int(sys.argv[2]) )
    rclpy.spin_until_future_complete(client, future)
    response = future.result()
    client.get_logger().info(f"Result: {response.sum}")

    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

##  III. Create a custom message package
### 1. Create a new package for custom messages:
```bash
cd ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 msg_package
```
Note:
- it can only be an `ament_cmake` package
- You can create custom messages and services in the same package, but it is often better to separate them. It avoids unnecessary dependencies, circular dependencies problems, and makes it easier to reuse the message package across different projects. 
### 2. Create a custom message/service definition:
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

### 3. Update `CMakeLists.txt` to build messages and services:
```cmake
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Sphere.msg"
  "srv/CheckSphereOverlap.srv"
  DEPENDENCIES geometry_msgs
)
```
### 4. Add dependencies to `package.xml`:
- Add `geometry_msgs` as a runtime dependency
- Add `rosidl_default_generators` and `rosidl_default_runtime` as build and exec dependencies for message generation. 
- Add the package to the `rosidl_interface_packages` group.
```xml
<depend>geometry_msgs</depend>
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```
### 5. Build the package and source the workspace:
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

## IV. Create Parameter Package
All the steps are similar to the publisher-subscriber example, except:
- Step 2: you create a node that declares and uses parameters.
- Step 3: the dependencies in `package.xml` also include `rclpy` and `rcl_interfaces` for parameter APIs.
- Step 4: the console script in `setup.py` will be updated to point to the new parameter node.

## Step 2. Create a node that declares and uses parameters in `src/param_package/`:
<details>
<summary>py_package/src/minimal_parameter.py</summary>

```python
# param_node.py
import rclpy
from rclpy.node import Node

class MinimalParam(Node):
    def __init__(self):
        super().__init__('minimal_param_node')
        self.declare_parameter('my_param', 'default_value')
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        my_param = self.get_parameter('my_parameter')
        self.get_logger().info(f'my param value: {my_param.get_param_value().string_value}')
        new_param = rclpy.parameter.Parameter(
            'my_parameter',
            rclpy.Parameter.Type.STRING,
            'I modified Value'
            )
        all_new_params = [new_param]
        self.set_parameters(all_new_params)

def main():
    rclpy.init()
    node = MinimalParam()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```
<details>