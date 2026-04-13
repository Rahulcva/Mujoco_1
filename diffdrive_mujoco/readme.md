# 🚀 DiffDrive MuJoCo (ROS2 Integration)

A differential drive robot simulation using **MuJoCo + ROS2** with multiple modes:

* Pure MuJoCo simulation
* ROS2 integration
* Camera streaming (front & rear)
* Client-server architecture

---

# 🤖 Robot Model

The robot is defined in:

👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/differentialdrive.xml

### Features:

* Differential drive (left + right wheel)
* Front & rear cameras
* Caster wheel for stability
* Velocity-controlled actuators
* Ground plane + lighting setup

---

# 🧠 Simulation Modes

## 1️⃣ MuJoCo Only (No ROS)

Run:
👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/diff_drive.py

✔ Pure physics simulation
✔ No ROS required

---

## 2️⃣ ROS2 (Without Camera)

Run:
👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/diffdrive_ros2.py

✔ `/cmd_vel` control
✔ `/odom` publishing

---

## 3️⃣ ROS2 + Camera

Run:
👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/diff_drive_ros_camera.py

✔ Front + Rear camera streams
✔ Full ROS integration

---

## 4️⃣ Client-Server Architecture

Server:
👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/server.py

Client:
👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/client.py

✔ Remote control system
✔ Front & rear access handling

---

# 📡 ROS Topics

### Control

```
/cmd_vel
```

### Sensors

```
/odom
/front_camera/image_raw
/rear_camera/image_raw
```

### System

```
/parameter_events
/rosout
```

---

# 🎮 Control Example

```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}"
```

---

# 🧱 Key MuJoCo Concepts Used

From the robot model :

### 🔹 Joints

* `hinge` → used for wheels (rotation only)

### 🔹 Actuators

* `velocity` → direct wheel speed control

```python
data.ctrl[0] = left_wheel_speed
data.ctrl[1] = right_wheel_speed
```

### 🔹 Sensors

* `framepos` → robot position tracking

### 🔹 Cameras

* `front_cam`
* `rear_cam`

---

# ⚙️ Requirements

* ROS2 (Humble or newer)
* MuJoCo (Python bindings)
* Python 3.10+

---

# ▶️ Run

```bash
export MUJOCO_GL=egl
ros2 run diffdrive_mujoco diffdrive_node
```

---

# 🧠 Architecture

```
MuJoCo Physics
      ↓
Wheel Control (velocity)
      ↓
ROS2 Topics (/cmd_vel)
      ↓
Sensors + Cameras
      ↓
ROS Visualization / Client
```

---

# 💡 Highlights

* Clean MuJoCo + ROS2 integration
* Multi-mode simulation support
* Camera streaming pipeline
* Realistic differential drive behavior

---



---
