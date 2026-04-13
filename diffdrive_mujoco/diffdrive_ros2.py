import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import os

class DiffDriveNode(Node):

    def __init__(self):
        super().__init__('diffdrive_mujoco')

        # ROS
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        
        self.left_speed = 0.0
        self.right_speed = 0.0

        # MuJoCo
        xml_path = os.path.join(os.path.dirname(__file__), "differentialdrive.xml")
        self.model = mj.MjModel.from_xml_path(xml_path)
        self.data = mj.MjData(self.model)
        
        mj.set_mjcb_control(self.controller)

        # GLFW - all in main thread
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
            
        self.window = glfw.create_window(1200, 900, "Diff Drive", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
            
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        # MuJoCo rendering setup
        self.cam = mj.MjvCamera()
        self.opt = mj.MjvOption()
        mj.mjv_defaultCamera(self.cam)
        mj.mjv_defaultOption(self.opt)
        
        self.scene = mj.MjvScene(self.model, maxgeom=10000)
        self.mjr_context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150.value)
        
        self.cam.azimuth = 90
        self.cam.elevation = -45
        self.cam.distance = 5
        self.cam.lookat[:] = [0.0, 0.0, 0.0]

        # 🔥 Use ROS2 timer instead of thread - runs in main thread
        self.create_timer(1.0/60.0, self.sim_step)  # 60Hz

    def cmd_callback(self, msg):
        v = msg.linear.x
        w = msg.angular.z
        wheel_separation = 0.5
        self.left_speed = v - (w * wheel_separation / 2)
        self.right_speed = v + (w * wheel_separation / 2)

    def controller(self, model, data):
        data.ctrl[0] = float(np.clip(self.left_speed, -10, 10))
        data.ctrl[1] = float(np.clip(self.right_speed, -10, 10))

    def sim_step(self):
        """Called by ROS2 timer at 60Hz - runs in main thread"""
        if glfw.window_should_close(self.window):
            self.get_logger().info("Window closed, shutting down...")
            rclpy.shutdown()
            return

        # Step physics multiple times for stability
        time_prev = self.data.time
        while self.data.time - time_prev < 1.0/60.0:
            mj.mj_step(self.model, self.data)

        # Publish odometry
        self.publish_odom()

        # Render
        self.render()

        glfw.poll_events()

    def publish_odom(self):
        pos = self.data.qpos[0:3]
        quat = self.data.qpos[3:7]  # [w, x, y, z]

        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"
        
        odom.pose.pose.position.x = float(pos[0])
        odom.pose.pose.position.y = float(pos[1])
        odom.pose.pose.position.z = float(pos[2])
        
        # MuJoCo [w,x,y,z] to ROS [x,y,z,w]
        odom.pose.pose.orientation.w = float(quat[0])
        odom.pose.pose.orientation.x = float(quat[1])
        odom.pose.pose.orientation.y = float(quat[2])
        odom.pose.pose.orientation.z = float(quat[3])

        vel = self.data.qvel
        odom.twist.twist.linear.x = float(vel[0])
        odom.twist.twist.angular.z = float(vel[5])

        self.odom_pub.publish(odom)

    def render(self):
        viewport_width, viewport_height = glfw.get_framebuffer_size(self.window)
        viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)
        
        mj.mjv_updateScene(self.model, self.data, self.opt, None,
                          self.cam, mj.mjtCatBit.mjCAT_ALL.value, self.scene)
        mj.mjr_render(viewport, self.scene, self.mjr_context)
        glfw.swap_buffers(self.window)

    def destroy_node(self):
        glfw.destroy_window(self.window)
        glfw.terminate()
        super().destroy_node()

def main():
    rclpy.init()
    node = DiffDriveNode()
    try:
        rclpy.spin(node)  # This will call sim_step via timer
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()