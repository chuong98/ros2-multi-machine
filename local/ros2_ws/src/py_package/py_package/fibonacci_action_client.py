import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from msg_package.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__("Fibonacci_Action_Client")
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')
        self._send_goal_future = None

    def send_goal(self, order: int):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        self._action_client.wait_for_server()
        
        # return self._action_client.send_goal_async(goal_msg) # you can simply finish by sending the goal and done

        # this is to get the update while waiting
        goal_future = self._action_client.send_goal_async(goal_msg)
        if goal_future is not None:
            goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        goal_handler =future.result()
        if not goal_handler.accepted:
            self.get_logger().info('Goal rejected. X-X')
            return

        self.get_logger().info('Goal Accepted :)')
        result_future = goal_handler.get_result_async()
        if result_future is not None:
            result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

def main():
    rclpy.init()
    action_client = FibonacciActionClient()
    action_client.send_goal(10)
    rclpy.spin(action_client)
    # rclpy.spin_until_future_complete(action_client, future)

if __name__ == '__main__':
    main()