import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool
import time

class Client(Node):
    def __init__(self):
        super().__init__('client')
        self.cli = self.create_client(SetBool, 'select_camera')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

    def send(self, val):
        req = SetBool.Request()
        req.data = val

        future = self.cli.call_async(req)

        print("Request sent")
        print("I am NOT waiting 😎")   # async proof

        future.add_done_callback(self.callback)

    def callback(self, future):
        try:
            res = future.result()
            print("Response received:", res.message)
        except Exception as e:
            print("Error:", e)
        #for shutdown after result 
        time.sleep(0.5)
        rclpy.shutdown()   


def main():
    rclpy.init()
    node = Client()

    # 👇 USER INPUT
    val = int(input("Enter 1 (Front) or 0 (Rear): "))

    node.send(val == 1)

    rclpy.spin(node)


if __name__ == '__main__':
    main()