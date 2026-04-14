import mujoco as mj
import mujoco.viewer
import numpy as np
import os
import time
import threading
import tkinter as tk
from tkinter import ttk
import cv2

# -----------------------------
# GLOBAL CONTROL VARIABLES
# -----------------------------
left_speed = 0.0
right_speed = 0.0
running = True

# -----------------------------
# LOAD MODEL
# -----------------------------
xml_path = os.path.join(os.path.dirname(__file__), "differentialdrive.xml")

model = mj.MjModel.from_xml_path(xml_path)
data = mj.MjData(model)

data.ctrl[0] = 0
data.ctrl[1] = 0

# -----------------------------
# CONTROLLER
# -----------------------------
def controller(model, data):
    global left_speed, right_speed

    l = np.clip(left_speed, -10, 10)
    r = np.clip(right_speed, -10, 10)

    data.ctrl[0] = float(l)
    data.ctrl[1] = float(r)

mj.set_mjcb_control(controller)

# -----------------------------
# GUI
# -----------------------------
def create_gui():
    global left_speed, right_speed, running

    root = tk.Tk()
    root.title("Robot Control")
    root.geometry("250x300")

    def set_speed(l, r):
        global left_speed, right_speed
        left_speed = l
        right_speed = r

    ttk.Button(root, text="Forward", command=lambda:set_speed(2,2)).pack(fill="x")
    ttk.Button(root, text="Backward", command=lambda:set_speed(-2,-2)).pack(fill="x")
    ttk.Button(root, text="Left", command=lambda:set_speed(-1,1)).pack(fill="x")
    ttk.Button(root, text="Right", command=lambda:set_speed(1,-1)).pack(fill="x")
    ttk.Button(root, text="STOP", command=lambda:set_speed(0,0)).pack(fill="x")

    def on_close():
        global running
        running = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

# -----------------------------
# MAIN
# -----------------------------
def main():
    global running

    threading.Thread(target=create_gui, daemon=True).start()

    # Depth renderer
    depth_renderer = mj.Renderer(model)
    depth_renderer.enable_depth_rendering()

    # Segmentation renderer
    seg_renderer = mj.Renderer(model)
    seg_renderer.enable_segmentation_rendering()

    with mujoco.viewer.launch_passive(model, data) as viewer:

        print("Simulation Started")
        print("WASD or GUI to control")

        while viewer.is_running() and running:

            mj.mj_step(model, data)

            # ---------------- DEPTH ----------------
            depth_renderer.update_scene(data)
            depth = depth_renderer.render()

            depth -= depth.min()
            depth /= 2 * depth[depth <= 1].mean()
            depth_pixels = (255 * np.clip(depth, 0, 1)).astype(np.uint8)

            # ---------------- SEGMENTATION ----------------
            seg_renderer.update_scene(data)
            seg = seg_renderer.render()

            geom_ids = seg[:, :, 0].astype(np.float64) + 1
            geom_ids = geom_ids / geom_ids.max()
            seg_pixels = (255 * geom_ids).astype(np.uint8)

            # ---------------- SHOW WINDOWS ----------------
            cv2.imshow("Depth", depth_pixels)
            cv2.imshow("Segmentation", seg_pixels)
            cv2.waitKey(1)

            viewer.sync()
            time.sleep(0.001)

    cv2.destroyAllWindows()
    print("Simulation ended")

if __name__ == "__main__":
    main()
