import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subcriber')
        self.subcriber_ = self.create_subscription(String,'topic',self.listener_callback, qos_profile=10)
        self.subcriber_ # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    subscriber = MinimalSubscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()  

