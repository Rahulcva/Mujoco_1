# import mujoco as mj
# from mujoco.glfw import glfw
# import numpy as np
# import os
# import threading
# import tkinter as tk

# # -----------------------------
# # GLOBAL CONTROL VARIABLES
# # -----------------------------
# left_speed = 0.0
# right_speed = 0.0

# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# xml_path = os.path.join(os.path.dirname(__file__), "differentialdrive.xml")

# model = mj.MjModel.from_xml_path(xml_path)
# data = mj.MjData(model)

# # 🔥 FORCE INITIAL STOP
# data.ctrl[0] = 0
# data.ctrl[1] = 0

# cam = mj.MjvCamera()
# opt = mj.MjvOption()

# # -----------------------------
# # CONTROLLER
# # -----------------------------
# def controller(model, data):
#     global left_speed, right_speed

#     l = np.clip(left_speed, -10, 10)
#     r = np.clip(right_speed, -10, 10)

#     data.ctrl[0] = float(l)
#     data.ctrl[1] = float(r)

# mj.set_mjcb_control(controller)

# # -----------------------------
# # TKINTER GUI
# # -----------------------------
# def gui_thread():
#     global left_speed, right_speed

#     root = tk.Tk()
#     root.title("Robot Control")

#     def set_speed(l, r):
#         global left_speed, right_speed
#         left_speed = l
#         right_speed = r

#     set_speed(0, 0)

#     def forward():
#         set_speed(8, 8)

#     def backward():
#         set_speed(-8, -8)

#     def left():
#         set_speed(-4, 4)

#     def right():
#         set_speed(4, -4)

#     def stop():
#         set_speed(0, 0)

#     tk.Button(root, text="Forward", command=forward).pack()
#     tk.Button(root, text="Backward", command=backward).pack()
#     tk.Button(root, text="Left", command=left).pack()
#     tk.Button(root, text="Right", command=right).pack()
#     tk.Button(root, text="Stop", command=stop).pack()

#     root.mainloop()

# left_speed = 0
# right_speed = 0

# threading.Thread(target=gui_thread, daemon=True).start()

# # -----------------------------
# # MUJOCO WINDOW SETUP
# # -----------------------------
# glfw.init()
# window = glfw.create_window(1200, 900, "Diff Drive", None, None)
# glfw.make_context_current(window)
# glfw.swap_interval(1)

# mj.mjv_defaultCamera(cam)
# mj.mjv_defaultOption(opt)

# scene = mj.MjvScene(model, maxgeom=10000)
# context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

# cam.azimuth = 90
# cam.elevation = -45
# cam.distance = 5
# cam.lookat = np.array([0, 0, 0])

# # -----------------------------
# # 🔥 POSITION PRINT CONTROL
# # -----------------------------
# last_print_time = 0

# # -----------------------------
# # SIMULATION LOOP
# # -----------------------------
# while not glfw.window_should_close(window):

#     time_prev = data.time

#     while data.time - time_prev < 1.0/60.0:
#         mj.mj_step(model, data)

#     # 🔥 GET CURRENT POSITION (MARKER SENSOR)
#     if data.time - last_print_time > 0.2:
#         pos = data.sensordata[0:3]

#         print(f"Robot Position -> x: {pos[0]:.2f}, y: {pos[1]:.2f}")

#         last_print_time = data.time

#     viewport_width, viewport_height = glfw.get_framebuffer_size(window)
#     viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

#     mj.mjv_updateScene(model, data, opt, None, cam,
#                        mj.mjtCatBit.mjCAT_ALL.value, scene)

#     mj.mjr_render(viewport, scene, context)

#     glfw.swap_buffers(window)
#     glfw.poll_events()

# glfw.terminate()


import mujoco as mj
import mujoco.viewer
import numpy as np
import os
import time
import threading
import tkinter as tk
from tkinter import ttk

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

# FORCE INITIAL STOP
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
# TKINTER GUI THREAD
# -----------------------------
def create_gui():
    global left_speed, right_speed, running
    
    root = tk.Tk()
    root.title("🤖 Robot Control Panel")
    root.geometry("300x400")
    root.resizable(False, False)
    
    # Style
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=10)
    style.configure('Stop.TButton', font=('Arial', 14, 'bold'), foreground='red')
    
    # Title
    title_label = tk.Label(root, text="Differential Drive Robot", 
                          font=('Arial', 16, 'bold'), pady=10)
    title_label.pack()
    
    # Speed Display Frame
    speed_frame = tk.LabelFrame(root, text="Current Speeds", font=('Arial', 12), padx=10, pady=10)
    speed_frame.pack(padx=10, pady=5, fill='x')
    
    left_var = tk.StringVar(value="Left: 0.0")
    right_var = tk.StringVar(value="Right: 0.0")
    
    left_label = tk.Label(speed_frame, textvariable=left_var, font=('Arial', 12), fg='blue')
    left_label.pack(anchor='w')
    
    right_label = tk.Label(speed_frame, textvariable=right_var, font=('Arial', 12), fg='green')
    right_label.pack(anchor='w')
    
    # Position Display Frame
    pos_frame = tk.LabelFrame(root, text="Robot Position", font=('Arial', 12), padx=10, pady=10)
    pos_frame.pack(padx=10, pady=5, fill='x')
    
    x_var = tk.StringVar(value="X: 0.00")
    y_var = tk.StringVar(value="Y: 0.00")
    
    x_label = tk.Label(pos_frame, textvariable=x_var, font=('Arial', 12))
    x_label.pack(anchor='w')
    
    y_label = tk.Label(pos_frame, textvariable=y_var, font=('Arial', 12))
    y_label.pack(anchor='w')
    
    # Control Buttons Frame
    control_frame = tk.LabelFrame(root, text="Controls", font=('Arial', 12), padx=10, pady=10)
    control_frame.pack(padx=10, pady=5, fill='x')
    
    def update_display():
        left_var.set(f"Left: {left_speed:.1f}")
        right_var.set(f"Right: {right_speed:.1f}")
        
        # Get position from sensordata
        try:
            pos = data.sensordata[0:3]
            x_var.set(f"X: {pos[0]:.2f}")
            y_var.set(f"Y: {pos[1]:.2f}")
        except:
            pass
        
        if running:
            root.after(100, update_display)
    
    def set_speed(l, r):
        global left_speed, right_speed
        left_speed = l
        right_speed = r
    
    def forward():
        set_speed(2, 2)
    
    def backward():
        set_speed(-2, -2)
    
    def turn_left():
        set_speed(-1, 1)
    
    def turn_right():
        set_speed(1, -1)
    
    def stop():
        set_speed(0, 0)
    
    # Button Layout
    fwd_btn = ttk.Button(control_frame, text="⬆ Forward (W)", command=forward, width=20)
    fwd_btn.pack(pady=2)
    
    mid_frame = tk.Frame(control_frame)
    mid_frame.pack(pady=2)
    
    left_btn = ttk.Button(mid_frame, text="⬅ Left (A)", command=turn_left, width=12)
    left_btn.pack(side=tk.LEFT, padx=2)
    
    right_btn = ttk.Button(mid_frame, text="Right (D) ➡", command=turn_right, width=12)
    right_btn.pack(side=tk.LEFT, padx=2)
    
    back_btn = ttk.Button(control_frame, text="⬇ Backward (S)", command=backward, width=20)
    back_btn.pack(pady=2)
    
    stop_btn = ttk.Button(control_frame, text="⛔ STOP (Space)", command=stop, 
                         width=20, style='Stop.TButton')
    stop_btn.pack(pady=10)
    
    # Status bar
    status_label = tk.Label(root, text="MuJoCo Viewer Running", 
                           font=('Arial', 10), fg='gray', pady=5)
    status_label.pack(side=tk.BOTTOM)
    
    # Keyboard bindings for GUI window
    root.bind('<w>', lambda e: forward())
    root.bind('<W>', lambda e: forward())
    root.bind('<s>', lambda e: backward())
    root.bind('<S>', lambda e: backward())
    root.bind('<a>', lambda e: turn_left())
    root.bind('<A>', lambda e: turn_left())
    root.bind('<d>', lambda e: turn_right())
    root.bind('<D>', lambda e: turn_right())
    root.bind('<space>', lambda e: stop())
    
    # Start update loop
    update_display()
    
    # Handle close
    def on_closing():
        global running
        running = False
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

# -----------------------------
# MAIN SIMULATION
# -----------------------------
def main():
    global running
    
    # Start GUI in separate thread
    gui_thread = threading.Thread(target=create_gui, daemon=True)
    gui_thread.start()
    
    last_print_time = 0
    
    # Launch MuJoCo native viewer
    with mujoco.viewer.launch_passive(model, data) as viewer:
        
        print("=" * 60)
        print("🚀 MuJoCo Robot Simulation Started!")
        print("=" * 60)
        print("Controls:")
        print("  GUI Buttons or Keyboard:")
        print("    W / ⬆  = Forward")
        print("    S / ⬇  = Backward")
        print("    A / ⬅  = Turn Left")
        print("    D / ➡  = Turn Right")
        print("    Space  = STOP")
        print("=" * 60)
        
        while viewer.is_running() and running:
            # Step physics
            mj.mj_step(model, data)
            
            # Sync viewer
            viewer.sync()
            
            # Small delay to prevent maxing CPU
            time.sleep(0.001)
    
    print("\n✅ Simulation ended.")

if __name__ == "__main__":
    main()

