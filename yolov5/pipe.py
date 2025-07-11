import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import depthai as dai
import cv2
import torch
import numpy as np
import time
import os

# === ROS2 SETUP ===
rclpy.init()
node = rclpy.create_node('crack_detector')
pub = node.create_publisher(Twist, '/cmd_vel', 10)

# === MOVEMENT FUNCTIONS ===
def move_forward():
    twist = Twist()
    twist.linear.x = 0.1  # Adjust speed if needed
    pub.publish(twist)

def stop():
    twist = Twist()
    twist.linear.x = 0.0
    twist.angular.z = 0.0
    pub.publish(twist)

def reverse():
    twist = Twist()
    twist.linear.x = -0.05  # Small reverse
    pub.publish(twist)
    time.sleep(1.0)
    stop()

def turn_slightly():
    twist = Twist()
    twist.angular.z = 0.3  # Slight right turn
    pub.publish(twist)
    time.sleep(1.0)
    stop()

# === YOLO MODEL LOADING ===
model = torch.hub.load('.', 'custom', path='gcpc_model.pt', source='local')
model.conf = 0.5

# === DEPTHAI PIPELINE TO CONNECT CAMERA TO TURTLEBOT===
pipeline = dai.Pipeline()
cam_rgb = pipeline.create(dai.node.ColorCamera)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam_rgb.setInterleaved(False)

xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("video")
cam_rgb.video.link(xout.input)

# === MAIN LOOP ===
with dai.Device(pipeline) as device:
    q = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    print("Running autonomous crack detection...")

    while True:
        in_frame = q.get()
        frame = in_frame.getCvFrame()

        results = model(frame)
        detections = results.pandas().xyxy[0]

        if len(detections) > 0:
            print("Crack detected!")
            stop()
            reverse()
            turn_slightly()

            # Saves image
            filename = f"crack_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")

            time.sleep(1.5) #Stops to scan
            move_forward()
        else:
            move_forward()

        # Optional: Enable this if you want a GUI feed
        # cv2.imshow("Frame", frame)
        # if cv2.waitKey(1) == ord('q'):
        #     break
