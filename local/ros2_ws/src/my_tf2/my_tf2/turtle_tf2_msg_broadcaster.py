from geometry_msgs.msg import PointStamped, Twist

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn

class PointPublisher(Node):
    def __init__(self):
        super().__init__('turtle_tf2_msg_publisher')

        # spawn turtle
        self.spawner = self.create_client(Spawn, 'spawn')
        self.is_spawned = False
        self.spawn_result = None
        self.is_ready = False
        self.timer = self.create_timer(0.1, self.spawn_turtle)

        # pub/sub
        self.vel_pub = None
        self.sub = None
        self.pub = None

    def spawn_turtle(self):
        if self.is_ready:
            return 
        
        if self.spawn_result:
            if self.is_spawned:
                # ready to subcribe
                self.vel_pub = self.create_publisher(Twist, 'turtle3/cmd_vel', 10)
                self.sub = self.create_subscription(Pose, 'turtle3/pose', self.handle_turtle_pose, 10)
                self.pub = self.create_publisher(PointStamped, 'turtle3/turtle_point_stamped', 10)
                self.is_ready = True
            else:
                if self.spawn_result.done():
                    self.is_spawned = True
                    self.get_logger().info('Turtle 3 is spawned')
                else:
                    self.get_logger().info('Spawn is not finished')
        else:
            if self.spawner.service_is_ready():
                request = Spawn.Request()           
                request.name = 'turtle3'
                request.x = 4.0
                request.y = 3.0
                request.theta = 0.0
                self.spawn_result = self.spawner.call_async(request)
            else:
                self.get_logger().info('Spawn Turtle3 is not ready')

    def handle_turtle_pose(self, msg: Pose):
        # Publish the cmd velocity to make the turtle run in a circle
        vel_msg = Twist()
        vel_msg.linear.x = 1.0
        vel_msg.angular.z = 1.0
        self.vel_pub.publish(vel_msg)

        # Publish the current position of the turtle3
        ps = PointStamped()
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.header.frame_id = 'world'
        ps.point.x = msg.x
        ps.point.y = msg.y
        ps.point.z = 0.0
        self.pub.publish(ps)

def main():
    rclpy.init()
    node = PointPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()