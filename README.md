# 🚀 DiffDrive MuJoCo (ROS2 Integration)

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![MuJoCo](https://img.shields.io/badge/MuJoCo-Simulator-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

A modular **differential drive robot simulation framework** built using **MuJoCo + ROS2**, extended with **depth sensing, segmentation, and tracking** for perception-driven robotics research.

This project is designed to bridge the gap between **low-level control**, **simulation physics**, and **high-level perception + decision-making (agentic AI)**.

---

# ✨ Key Features

- Differential drive kinematics with velocity control  
- Seamless ROS2 integration (`/cmd_vel`, `/odom`)  
- Front & rear camera streaming  
- Depth map generation from simulation  
- Pixel-wise segmentation pipeline  
- Real-time object tracking  
- Client-server architecture for remote control  
- Multi-mode execution (modular design)  

---

# 🤖 Robot Model

The robot is defined in:

👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/differentialdrive.xml  

## 🔧 Components

- **Drive System**  
  - Two powered wheels (left & right)  
  - Differential velocity control  

- **Support System**  
  - Passive caster wheel for balance  

- **Sensors**  
  - Frame position (`framepos`) for odometry  
  - Dual RGB cameras (front & rear)  
  - Depth-enabled rendering  

- **Environment**  
  - Ground plane  
  - Lighting for realistic rendering  

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

✔ Front & rear camera streaming  
✔ ROS image topics publishing  
✔ Real-time visualization  

---

## 4️⃣ Client-Server Architecture

Server:
👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/server.py  

Client:
👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/client.py  

✔ Remote execution support  
✔ Distributed control system  
✔ Multi-client interaction capability  

---

## 5️⃣ Depth + Segmentation

👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/diff_drive_depth_segmentaion.py  

### 🔍 Description

This module introduces a **perception layer** on top of simulation.

### ✔ Capabilities

- Depth map extraction from MuJoCo renderer  
- Pixel-level segmentation of scene  
- Object boundary understanding  
- Environment structure awareness  

### 🎯 Use Cases

- Obstacle detection  
- Scene understanding  
- Navigation planning  

---

## 6️⃣ Depth + Segmentation + Tracking

👉 https://github.com/Rahulcva/Mujoco_1/blob/main/diffdrive_mujoco/diff_drive_depth_segmentaion_camera_track.py  

### 🔍 Description

Extends perception with **real-time tracking and decision-making**.

### ✔ Capabilities

- Target detection via segmentation  
- Depth-assisted localization  
- Continuous object tracking  
- Camera-based following behavior  

### 🧠 Insight

This mode enables a **closed-loop perception → action system**, forming the base for **agentic robotics**.

---

## 📡 ROS Topics

### Control

/cmd_vel


### Sensors

/odom
/front_camera/image_raw
/rear_camera/image_raw


### Perception (Extended)

/depth_map
/segmentation_mask
/tracked_object


### System

/parameter_events
/rosout


---

## 🎮 Control Example


ros2 topic pub -r 10 /cmd_vel geometry_msgs/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}"

🧱 Core MuJoCo Concepts
🔹 Joints
hinge → wheel rotation
🔹 Actuators
velocity → direct speed control
data.ctrl[0] = left_wheel_speed
data.ctrl[1] = right_wheel_speed
🔹 Sensors
framepos → robot pose
Depth rendering → per-pixel distance
🔹 Cameras
front_cam
rear_cam
Depth-enabled rendering


🧠 System Architecture

MuJoCo Physics
      ↓
Wheel Control (velocity)
      ↓
ROS2 Interface (/cmd_vel)
      ↓
Sensors + Cameras
      ↓
Depth + Segmentation
      ↓
Tracking / Decision Layer
      ↓
Visualization / Client

⚙️ Requirements
ROS2 (Humble or newer)
MuJoCo (Python bindings)
Python 3.10+
🚀 Getting Started
git clone https://github.com/Rahulcva/Mujoco_1.git
cd Mujoco_1/diffdrive_mujoco
pip install -r requirements.txt

Run any mode:
python3 diff_drive.py
🔬 Research Relevance

This project bridges:
Simulation → Perception → Action


📌 Applications
Autonomous navigation
Obstacle avoidance
Visual servoing
Target following
Embodied AI research



👨‍💻 Authors

Aachal Sharma & Rahul 🚀
