import math

from geometry_msgs.msg import TransformStamped

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster


class LocalFramePublisher(Node):
    def __init__(self):
        super().__init__('carrot_tf2_broadcaster')

        # declara parameters
        self.turtle_name = self.declare_parameter('turtle_name', 'turtle1').get_parameter_value().string_value
        self.target_name = self.declare_parameter('target_frame', 'carrot1',).get_parameter_value().string_value
        self.target_radius = self.declare_parameter('target_radius', 1.0).get_parameter_value().double_value

        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.publish_target_frame)

    def publish_target_frame(self):
        seconds = self.get_clock().now().seconds_nanoseconds()[0]
        x = seconds*math.pi

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()

        t.header.frame_id = self.turtle_name
        t.child_frame_id = self.target_name

        # Turtle only exists in 2D, thus we get x and y translation
        # coordinates and set the z coordinate to 0
        t.transform.translation.x = self.target_radius*math.cos(x)
        t.transform.translation.y = self.target_radius*math.sin(x)
        t.transform.translation.z = 0.0

        # note, it will throw error if you set  0 instead of 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        # Send the transformation
        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = LocalFramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()

if __name__ == "__main__":
    main()