import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraServer(Node):

    def __init__(self):
        super().__init__('camera_server')

        self.bridge = CvBridge()

        # service
        self.create_service(SetBool, 'select_camera', self.callback)

        # camera topics
        self.create_subscription(Image, '/front_camera/image_raw', self.front_cb, 10)
        self.create_subscription(Image, '/rear_camera/image_raw', self.rear_cb, 10)

        self.current = None
        self.front_frame = None
        self.rear_frame = None

    def callback(self, request, response):
        if request.data:
            self.current = "front"
            self.get_logger().info("FRONT selected")
            response.message = "Front camera ON"
        else:
            self.current = "rear"
            self.get_logger().info("REAR selected")
            response.message = "Rear camera ON"

        response.success = True
        return response

    def front_cb(self, msg):
        self.front_frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

    def rear_cb(self, msg):
        self.rear_frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

    def run(self):
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.01)

            if self.current == "front" and self.front_frame is not None:
                cv2.imshow("Camera", self.front_frame)

            elif self.current == "rear" and self.rear_frame is not None:
                cv2.imshow("Camera", self.rear_frame)

            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()


def main():
    rclpy.init()
    node = CameraServer()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()