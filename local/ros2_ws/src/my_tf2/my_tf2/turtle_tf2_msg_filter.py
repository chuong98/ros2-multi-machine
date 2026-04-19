from collections import deque

from geometry_msgs.msg import PointStamped

import rclpy
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.time import Time

from tf2_ros import Buffer, TransformException, TransformListener

# Needed so Buffer.transform knows how to transform PointStamped.
import tf2_geometry_msgs  # noqa: F401


class PoseDrawer(Node):
	def __init__(self):
		super().__init__('turtle_tf2_pose_drawer')

		self.target_frame = self.declare_parameter(
			'target_frame', 'turtle1').get_parameter_value().string_value

		self.tf_buffer = Buffer()
		self.tf_listener = TransformListener(self.tf_buffer, self)

		self.queue_size = 10000
		self.buffer_timeout = Duration(seconds=1.0)
		self.max_message_age = Duration(seconds=10.0)
		self.pending_points = deque(maxlen=self.queue_size)

		self.point_sub = self.create_subscription(
			PointStamped,
			'/turtle3/turtle_point_stamped',
			self.enqueue_point,
			10)

		# Process queued messages frequently and transform only when TF is ready.
		self.process_timer = self.create_timer(0.02, self.process_queue)

	def enqueue_point(self, msg: PointStamped):
		if len(self.pending_points) == self.queue_size:
			self.get_logger().warn('Point queue full, dropping oldest message')
		self.pending_points.append(msg)

	def process_queue(self):
		while self.pending_points:
			point_msg = self.pending_points[0]

			if self._is_too_old(point_msg):
				self.pending_points.popleft()
				self.get_logger().warn('Dropping stale point message')
				continue

			try:
				if not self.tf_buffer.can_transform(
					self.target_frame,
					point_msg.header.frame_id,
					Time.from_msg(point_msg.header.stamp),
					self.buffer_timeout,
				):
					# Keep order like MessageFilter: wait until transform is available.
					return

				point_out = self.tf_buffer.transform(
					point_msg,
					self.target_frame,
					timeout=self.buffer_timeout,
				)
				self.get_logger().info(
					(
						'Point of turtle3 in frame of %s: '
						'x:%f y:%f z:%f'
					)
					% (
						self.target_frame,
						point_out.point.x,
						point_out.point.y,
						point_out.point.z,
					)
				)
				self.pending_points.popleft()
			except TransformException as ex:
				# Keep the message for future retries unless it becomes stale.
				self.get_logger().warn(f'Failure {ex}')
				return

	def _is_too_old(self, msg: PointStamped) -> bool:
		msg_time = Time.from_msg(msg.header.stamp)
		return (self.get_clock().now() - msg_time) > self.max_message_age


def main():
	rclpy.init()
	node = PoseDrawer()
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	finally:
		node.destroy_node()
		rclpy.shutdown()


if __name__ == '__main__':
	main()