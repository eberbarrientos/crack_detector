# Crack Detector for pipes

This project uses a TurtleBot4 equipped with an OAK-D camera and a YOLOv5 deep learning model to detect cracks in civil engineering pipes. When a crack is detected, the robot stops, saves an image, and resumes autonomous movement.

## 🔧 Features
- Real-time crack detection using a custom YOLOv5 model
- Built-in DepthAI and OpenCV integration
- ROS 2 Twist publishing for motion control
- Automatic image saving when cracks are detected

## 📁 Project Structure

crack_detector/

├── yolov5/

│    ├── pipe.py # Main Python script

│    └── pipe_model.pt # Trained YOLOv5 model

├── requirements.txt

└── README.md

## Requirements

- ROS 2 Humble (for `rclpy`, `geometry_msgs`)
- DepthAI-compatible camera (like OAK-D) configured via DepthAI SDK
- Python packages (see `requirements.txt`)

This project assumes that:
- The robot is configured to move using `/cmd_vel`
- The DepthAI camera is properly set up and streaming

## 📦 Model Weights

Download the trained YOLOv5 model for crack detection here:

- 🔗 https://drive.google.com/file/d/1fJFDjmr2ymGeb7JehBq-PMvYtP1FWyu4/view?usp=share_link
After downloading, place it in the 'yolov5/' directory of the project.

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/eberbarrientos/crack_detector.git
   cd crack_detector

2. Install dependencies:
    pip install -r requirements.txt

3. Run the script on your robot:
    python3 yolov5/pipe.py

🎓 Research Use Case

This project was built for use by the Civil Engineering department at UTA to explore autonomous inspection of PVC, concrete, and metal pipes.

🤖 Hardware

- TurtleBot4
- OAK-D camera

📷 Dataset

- Custom dataset of ~18,000 annotated pipe images (metal, concrete, some PVC)
- Trained using YOLOv5 with 10 epochs

🧠 Model

YOLOv5 (pipe_model.pt)
