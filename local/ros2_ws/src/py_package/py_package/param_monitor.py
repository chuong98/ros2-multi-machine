import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.parameter import Parameter, parameter_value_to_python
from rclpy.parameter_event_handler import ParameterEventHandler

class ParamMonitor(Node):
    def __init__(self):
        super().__init__('param_monitor_node')
        self.declare_parameter('an_int_param', 0)
        self.handler = ParameterEventHandler(self)

        self.callback_handle = self.handler.add_parameter_callback(
            parameter_name='an_int_param',
            node_name='param_monitor_node',
            callback=self.callback
        )

    def callback(self, p: Parameter):
        self.get_logger().info(f'Receiving an update to parameter: {p.name}: {parameter_value_to_python(p.value)}')

def main():
    rclpy.init()
    node = ParamMonitor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()