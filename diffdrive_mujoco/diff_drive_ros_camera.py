# import rclpy
# from rclpy.node import Node
# from geometry_msgs.msg import Twist
# from nav_msgs.msg import Odometry
# from sensor_msgs.msg import Image

# import mujoco as mj
# from mujoco.glfw import glfw
# import numpy as np
# import os

# class DiffDriveNode(Node):

#     def __init__(self):
#         super().__init__('diffdrive_mujoco')

#         # ROS
#         self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
#         self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
#         self.front_cam_pub = self.create_publisher(Image, '/front_camera/image_raw', 10)
#         self.top_cam_pub = self.create_publisher(Image, '/rear_camera/image_raw', 10)

#         self.left_speed = 0.0
#         self.right_speed = 0.0

#         # MuJoCo model
#         xml_path = os.path.join(os.path.dirname(__file__), "differentialdrive.xml")
#         self.model = mj.MjModel.from_xml_path(xml_path)
#         self.data = mj.MjData(self.model)

#         # -----------------------------
#         # ✅ GLFW FIRST
#         # -----------------------------
#         if not glfw.init():
#             raise RuntimeError("Failed to initialize GLFW")

#         self.window = glfw.create_window(1200, 900, "Diff Drive", None, None)
#         if not self.window:
#             glfw.terminate()
#             raise RuntimeError("Failed to create GLFW window")

#         glfw.make_context_current(self.window)
#         glfw.swap_interval(1)

#         # -----------------------------
#         # MuJoCo visualization
#         # -----------------------------
#         self.cam = mj.MjvCamera()
#         self.opt = mj.MjvOption()
#         mj.mjv_defaultCamera(self.cam)
#         mj.mjv_defaultOption(self.opt)

#         self.scene = mj.MjvScene(self.model, maxgeom=10000)
#         self.mjr_context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150.value)

#         self.cam.azimuth = 90
#         self.cam.elevation = -45
#         self.cam.distance = 5
#         self.cam.lookat[:] = [0.0, 0.0, 0.0]

#         # -----------------------------
#         # ✅ Renderer (lazy)
#         # -----------------------------
#         self.renderer = None

#         # -----------------------------
#         # ✅ Controller LAST
#         # -----------------------------
#         mj.set_mjcb_control(self.controller)

#         # Timer
#         self.create_timer(1.0/60.0, self.sim_step)

#     def cmd_callback(self, msg):
#         v = msg.linear.x
#         w = msg.angular.z
#         wheel_separation = 0.5
#         self.left_speed = v - (w * wheel_separation / 2)
#         self.right_speed = v + (w * wheel_separation / 2)

#     def controller(self, model, data):
#         data.ctrl[0] = float(np.clip(self.left_speed, -10, 10))
#         data.ctrl[1] = float(np.clip(self.right_speed, -10, 10))

#     def sim_step(self):
#         if glfw.window_should_close(self.window):
#             self.get_logger().info("Window closed, shutting down...")
#             rclpy.shutdown()
#             return

#         time_prev = self.data.time
#         while self.data.time - time_prev < 1.0/60.0:
#             mj.mj_step(self.model, self.data)

#         self.publish_odom()

#         self.render()              # 👈 FIRST (important)
#         self.publish_cameras()     # 👈 THEN camera

#         glfw.poll_events()

#     def publish_cameras(self):
#         try:
#             if self.renderer is None:
#                 self.renderer = mj.Renderer(self.model, width=640, height=480)

#             # FRONT CAMERA
#             self.renderer.update_scene(self.data, camera="front_cam")
#             img_front = self.renderer.render().copy()   # 🔥 copy important

#             msg = Image()
#             msg.header.stamp = self.get_clock().now().to_msg()
#             msg.height, msg.width = img_front.shape[:2]
#             msg.encoding = "rgb8"
#             msg.step = msg.width * 3
#             msg.data = img_front.tobytes()
#             self.front_cam_pub.publish(msg)

#             # 🔥 RESET (VERY IMPORTANT)
#             self.renderer.update_scene(self.data)

#             # REAR / TOP CAMERA
#             self.renderer.update_scene(self.data, camera="rear_cam")
#             img_top = self.renderer.render().copy()   # 🔥 copy important

#             msg2 = Image()
#             msg2.header.stamp = self.get_clock().now().to_msg()
#             msg2.height, msg2.width = img_top.shape[:2]
#             msg2.encoding = "rgb8"
#             msg2.step = msg2.width * 3
#             msg2.data = img_top.tobytes()
#             self.top_cam_pub.publish(msg2)

#         except Exception as e:
#             self.get_logger().error(f"Camera error: {e}")

#     def publish_odom(self):
#         pos = self.data.qpos[0:3]
#         quat = self.data.qpos[3:7]

#         odom = Odometry()
#         odom.header.stamp = self.get_clock().now().to_msg()
#         odom.header.frame_id = "odom"
#         odom.child_frame_id = "base_link"

#         odom.pose.pose.position.x = float(pos[0])
#         odom.pose.pose.position.y = float(pos[1])
#         odom.pose.pose.position.z = float(pos[2])

#         odom.pose.pose.orientation.w = float(quat[0])
#         odom.pose.pose.orientation.x = float(quat[1])
#         odom.pose.pose.orientation.y = float(quat[2])
#         odom.pose.pose.orientation.z = float(quat[3])

#         vel = self.data.qvel
#         odom.twist.twist.linear.x = float(vel[0])
#         odom.twist.twist.angular.z = float(vel[5])

#         self.odom_pub.publish(odom)

#     def render(self):
#         viewport_width, viewport_height = glfw.get_framebuffer_size(self.window)
#         viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

#         mj.mjv_updateScene(self.model, self.data, self.opt, None,
#                            self.cam, mj.mjtCatBit.mjCAT_ALL.value, self.scene)
#         mj.mjr_render(viewport, self.scene, self.mjr_context)
#         glfw.swap_buffers(self.window)

#     def destroy_node(self):
#         glfw.destroy_window(self.window)
#         glfw.terminate()
#         super().destroy_node()


# def main():
#     rclpy.init()
#     node = DiffDriveNode()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()


# if __name__ == '__main__':
#     main()


#forward movement - ros2 topic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}"


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image

import mujoco as mj
from mujoco import viewer
import numpy as np
import os


class DiffDriveNode(Node):

    def __init__(self):
        super().__init__('diffdrive_mujoco')

        # -----------------------------
        # ROS
        # -----------------------------
        self.cmd_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10
        )

        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.front_cam_pub = self.create_publisher(Image, '/front_camera/image_raw', 10)
        self.rear_cam_pub = self.create_publisher(Image, '/rear_camera/image_raw', 10)

        self.left_speed = 0.0
        self.right_speed = 0.0

        # -----------------------------
        # MuJoCo Model
        # -----------------------------
        xml_path = os.path.join(os.path.dirname(__file__), "differentialdrive.xml")
        self.model = mj.MjModel.from_xml_path(xml_path)
        self.data = mj.MjData(self.model)

        # -----------------------------
        # Viewer (PASSIVE ✅)
        # -----------------------------
        self.viewer = viewer.launch_passive(self.model, self.data)

        # -----------------------------
        # Offscreen renderer (for ROS cams)
        # -----------------------------
        self.renderer = mj.Renderer(self.model, width=640, height=480)

        # -----------------------------
        # Controller
        # -----------------------------
        mj.set_mjcb_control(self.controller)

        # Timer
        self.create_timer(1.0 / 60.0, self.sim_step)

    # -----------------------------
    def cmd_callback(self, msg):
        v = msg.linear.x
        w = msg.angular.z
        wheel_separation = 0.5

        self.left_speed = v - (w * wheel_separation / 2)
        self.right_speed = v + (w * wheel_separation / 2)

    # -----------------------------
    def controller(self, model, data):
        data.ctrl[0] = float(np.clip(self.left_speed, -10, 10))
        data.ctrl[1] = float(np.clip(self.right_speed, -10, 10))

    # -----------------------------
    def sim_step(self):
        if not self.viewer.is_running():
            self.get_logger().info("Viewer closed, shutting down...")
            rclpy.shutdown()
            return

        time_prev = self.data.time

        while self.data.time - time_prev < 1.0 / 60.0:
            mj.mj_step(self.model, self.data)

        # sync viewer (VERY IMPORTANT)
        self.viewer.sync()

        self.publish_odom()
        self.publish_cameras()

    # -----------------------------
    def publish_cameras(self):
        try:
            # FRONT
            self.renderer.update_scene(self.data, camera="front_cam")
            img_front = self.renderer.render().copy()

            msg = Image()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.height, msg.width = img_front.shape[:2]
            msg.encoding = "rgb8"
            msg.step = msg.width * 3
            msg.data = img_front.tobytes()
            self.front_cam_pub.publish(msg)

            # RESET
            self.renderer.update_scene(self.data)

            # REAR
            self.renderer.update_scene(self.data, camera="rear_cam")
            img_rear = self.renderer.render().copy()

            msg2 = Image()
            msg2.header.stamp = self.get_clock().now().to_msg()
            msg2.height, msg2.width = img_rear.shape[:2]
            msg2.encoding = "rgb8"
            msg2.step = msg2.width * 3
            msg2.data = img_rear.tobytes()
            self.rear_cam_pub.publish(msg2)

        except Exception as e:
            self.get_logger().error(f"Camera error: {e}")

    # -----------------------------
    def publish_odom(self):
        pos = self.data.qpos[0:3]
        quat = self.data.qpos[3:7]

        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        odom.pose.pose.position.x = float(pos[0])
        odom.pose.pose.position.y = float(pos[1])
        odom.pose.pose.position.z = float(pos[2])

        odom.pose.pose.orientation.w = float(quat[0])
        odom.pose.pose.orientation.x = float(quat[1])
        odom.pose.pose.orientation.y = float(quat[2])
        odom.pose.pose.orientation.z = float(quat[3])

        vel = self.data.qvel
        odom.twist.twist.linear.x = float(vel[0])
        odom.twist.twist.angular.z = float(vel[5])
                                           

        self.odom_pub.publish(odom)

    # -----------------------------
    def destroy_node(self):
        self.viewer.close()
        super().destroy_node()


# -----------------------------
def main():
    rclpy.init()
    node = DiffDriveNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()