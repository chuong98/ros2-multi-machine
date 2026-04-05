import rclpy
from rclpy.node import Node


class MinimalParam(Node):
    def __init__(self):
        super().__init__('minimal_param_node')
        self.declare_parameter('my_param', 'default_value')
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        my_param = self.get_parameter('my_param')
        self.get_logger().info(f'my param value: {my_param.get_parameter_value().string_value}')
        new_param = rclpy.parameter.Parameter(
            'my_param',
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