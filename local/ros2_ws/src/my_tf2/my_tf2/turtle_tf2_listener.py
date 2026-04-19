import math
from geometry_msgs.msg import Twist

import rclpy
from rclpy.node import Node

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros import TransformListener

from turtlesim.srv import Spawn

class FrameListener(Node):
    def __init__(self):
        super().__init__('turtle_tf2_listener')

        #declare and acquire target_frame parameter
        self.target_frame = self.declare_parameter('target_frame', 'turtle1').get_parameter_value().string_value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # create a client to spawn a turtle
        self.spawner = self.create_client(Spawn, 'spawn')
        self.spawn_ready = False # if the spawn service is ready
        self.is_spawned = False # if the turtle is spawned

        # speed publisher
        self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 1)

        # call on_timer every second
        self.timer = self.create_timer(1.0, self.on_timer)
        self.result = None

    def on_timer(self):
        from_frame_rel = self.target_frame
        to_frame_rel = 'turtle2'

        if self.spawn_ready:
            if self.is_spawned:
                # look up for the transformation between target_frame and turtle2_frames
                t = None
                try:
                    # time_stamp = rclpy.time.Time()  # get the latest available transform
                    # if self.tf_buffer.can_transform(to_frame_rel, from_frame_rel, time_stamp, time_out):
                    #     t = self.tf_buffer.lookup_transform(to_frame_rel, from_frame_rel, time_stamp, time_out)   
                    
                    # see here: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Time-Travel-With-Tf2-Cpp.html
                    # get the transform at a specific time, relatively to current frame
                    time_stamp = self.get_clock().now()  - rclpy.duration.Duration(seconds=5.0)  # get the transform at a specific time
                    time_out = rclpy.duration.Duration(seconds=1.0)  # wait for 1 second
                    if self.tf_buffer.can_transform_full(to_frame_rel, rclpy.time.Time(), from_frame_rel, time_stamp, 'world', time_out):
                        t = self.tf_buffer.lookup_transform_full(to_frame_rel, rclpy.time.Time(), from_frame_rel, time_stamp, 'world', time_out)
                except TransformException as ex:
                    self.get_logger().info(
                        f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}'
                    )
                    return
                if t is None:
                    self.get_logger().info(f'Cannot transform {to_frame_rel} to {from_frame_rel} at time {time_stamp}')
                    return

                # write speed cmd to reach the target_frame
                msg = Twist()
                scale_rotation_rate, scale_forward_speed = 1.0, 0.5
                angle = math.atan2(t.transform.translation.y, t.transform.translation.x)
                distance = math.sqrt(t.transform.translation.x**2 + t.transform.translation.y**2)
                msg.angular.z = scale_rotation_rate * angle
                msg.linear.x = scale_forward_speed * distance # frontal speed, y is horizontal which is not applicable
                self.publisher.publish(msg)

            else:
                if self.result.done():
                    self.get_logger().info(f'Success spawned {self.result.result().name}') 
                    self.is_spawned = True
                else:
                    self.get_logger().info("Spawn is not finished") 

        else:
            if self.spawner.service_is_ready():
                request = Spawn.Request()  
                request.name = 'turtle2'
                request.x = float(4)
                request.y = float(2)
                request.theta = float(0)
                # call request
                self.result = self.spawner.call_async(request)
                self.spawn_ready = True
            else:
                self.get_logger().info('Service is not ready')


def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()