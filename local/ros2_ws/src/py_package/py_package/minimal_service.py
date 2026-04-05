from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_servicer')
        self.srv = self.create_service(AddTwoInts,'add_ints', self.service_callback)

    def service_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f"Request: a={request.a}, b={request.b}, response.sum = {response.sum}")
        return response
    
def main():
    rclpy.init()
    service = MinimalService()
    rclpy.spin(service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()