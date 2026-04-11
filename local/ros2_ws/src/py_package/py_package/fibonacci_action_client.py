import rclpy
from rclpy.node import Node
from rclpy.action.client import ClientGoalHandle
from rclpy.action import ActionClient
from msg_package.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__("Fibonacci Action Client")
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')