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

    