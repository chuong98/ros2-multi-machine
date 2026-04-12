# Minimal Package Example in ROS 2 with Python

## I. Publisher-Subscriber Example
<details>
<summary><strong>Step 1. Create a package with Python build type</strong></summary>

```bash
cd ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 py_package	--dependencies rclpy
```

</details>

<details>
<summary><strong>Step 2. Create publisher and subscriber nodes in <code>src/py_package/</code></strong></summary>

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

</details>

<details>
<summary><strong>Step 3. Add dependencies to <code>package.xml</code></strong></summary>

```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>std_msgs</exec_depend>
```

</details>

<details>
<summary><strong>Step 4. Add console scripts to <code>setup.py</code></strong></summary>

```python
entry_points={
	'console_scripts': [
		# executable_name = package_name.module_name:function_name
		'talker = py_package.publisher_node:main',
		'listener = py_package.subscriber_node:main',
	],
},
```

</details>

<details>
<summary><strong>Step 5. Build the package and source the workspace</strong></summary>

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

</details>

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

## III. Create action package
All the steps are similar to the publisher-subscriber example, except:
- Step 2: you create action server and client nodes.
- Step 3: the dependencies in `package.xml` also include `example_interfaces` for the action interface.
- Step 4: the console scripts in `setup.py` will be updated to point to the new action server and client nodes.
### Step 2. Create action server and client nodes in `src/py_package/`:
<details>           
<summary>fibonacci_action_server.py</summary>

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
import time
from msg_package.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self.get_logger().info('Start fibonacci action server')
        self._action_server = ActionServer(self, action_type=Fibonacci, action_name='fibonacci', execute_callback=self.execute_callback)
    
    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info('Executing goal')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0,1]

        # computing
        sequence = feedback_msg.partial_sequence

        for i in range(1, goal_handle.request.order):
            sequence.append(sequence[i] + sequence[i-1])
            self.get_logger().info(f'Feedback: {sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        # set result
        goal_handle.succeed() # if Goal state not set, assuming aborted.
        result = Fibonacci.Result()
        result.sequence = sequence
        self.get_logger().info('Finished goal')
        return result
    
def main():
    rclpy.init()
    action_server = FibonacciActionServer()
    rclpy.spin(action_server)

if __name__ == '__main__':
    main()
```
</details>


<details>           
<summary>fibonacci_action_client.py</summary>

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
import time
from msg_package.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self.get_logger().info('Start fibonacci action server')
        self._action_server = ActionServer(self, action_type=Fibonacci, action_name='fibonacci', execute_callback=self.execute_callback)
    
    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info('Executing goal')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0,1]

        # computing
        sequence = feedback_msg.partial_sequence

        for i in range(1, goal_handle.request.order):
            sequence.append(sequence[i] + sequence[i-1])
            self.get_logger().info(f'Feedback: {sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        # set result
        goal_handle.succeed() # if Goal state not set, assuming aborted.
        result = Fibonacci.Result()
        result.sequence = sequence
        self.get_logger().info('Finished goal')
        return result
    
def main():
    rclpy.init()
    action_server = FibonacciActionServer()
    rclpy.spin(action_server)

if __name__ == '__main__':
    main()
```
</details>

## IV. Create Parameter Package
All the steps are similar to the publisher-subscriber example, except:
- Step 2: you create a node that declares and uses parameters.
- Step 3: the dependencies in `package.xml` also include `rclpy` and `rcl_interfaces` for parameter APIs.
- Step 4: the console script in `setup.py` will be updated to point to the new parameter node.

### Step 2. Create a node that declares and uses parameters in `src/param_package/`:

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
</details>

