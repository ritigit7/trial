import cv2
from ultralytics import YOLO
import torch
from threading import Thread
import streamlit as st
import easyocr
import numpy as np


def capture_video(rtsp_url, queue):
    cap = cv2.VideoCapture(rtsp_url)
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to access the camera.")
            break
        queue.append(img)
    cap.release()


def video_detection(rtsp_url):
    classNames = ['Halmet', 'Mask', 'NO-Halmet', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone',
                  'Safety Vest', 'machinery', 'vehicle']

    model = YOLO("YOLO-Weights/ppe.pt").to('cuda')

    frame_queue = []
    capture_thread = Thread(target=capture_video, args=(rtsp_url, frame_queue))
    capture_thread.daemon = True
    capture_thread.start()

    while True:
        if len(frame_queue) == 0:
            continue 
        
        img = frame_queue.pop(0)
        img_resized = cv2.resize(img, (640, 480)) 
        results = model(img_resized, stream=True)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0]) 
                conf = round(float(box.conf[0]) * 100) / 100  
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name} {conf:.2f}'

                if class_name in ['Mask', 'Halmet', 'Safety Vest']:
                    color = (0, 255, 0)  
                elif class_name in ['NO-Halmet', 'NO-Mask', 'NO-Safety Vest']:
                    color = (0, 0, 255)  
                elif class_name in ['machinery', 'vehicle']:
                    color = (0, 149, 255)  
                else:
                    color = (85, 45, 255)  
                
                if conf > 0.5:  
                    cv2.rectangle(img_resized, (x1, y1), (x2, y2), color, 2)
                    t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                    c2 = (x1 + t_size[0], y1 - t_size[1] - 2)
                    cv2.rectangle(img_resized, (x1, y1), c2, color, -1, cv2.LINE_AA)  
                    cv2.putText(img_resized, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 255], 2)

        _, img_encoded = cv2.imencode('.jpg', img_resized)
        yield img_encoded.tobytes()


def number_plate_detection(rtsp_url):
    model = YOLO("YOLO-Weights/number_plate.pt").to('cuda')  
    reader = easyocr.Reader(['en']) 

    frame_queue = []
    capture_thread = Thread(target=capture_video, args=(rtsp_url, frame_queue))
    capture_thread.daemon = True
    capture_thread.start()

    while True:
        if len(frame_queue) == 0:
            continue 

        img = frame_queue.pop(0)
        img_resized = cv2.resize(img, (640, 480))
        results = model(img_resized, stream=True)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  
                conf = round(float(box.conf[0]) * 100) / 100  

                if conf > 0.5:  
                    plate_roi = img_resized[y1:y2, x1:x2]  

                    text_results = reader.readtext(plate_roi)
                    plate_number = text_results[0][-2] if text_results else "Unknown"

                    cv2.rectangle(img_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img_resized, plate_number, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        _, img_encoded = cv2.imencode('.jpg', img_resized)
        yield img_encoded.tobytes()




def main():

    st.sidebar.header("Camera Configuration")
    username = st.sidebar.text_input("Username", value="Test")
    password = st.sidebar.text_input("Password", value="Admin@123", type="password")
    # ip_address = st.sidebar.text_input("IP Address", value="172.27.4.28")
    camera_options = {
        "Store": "172.27.4.28",
        "Main Gate": "172.27.4.35",
        "Parking Road": "172.27.4.210",
        "Safety Check": "172.27.4.136"
    }
    selected_camera = st.sidebar.selectbox("Select Camera", options=list(camera_options.keys()))
    ip_address = camera_options[selected_camera]
    start_detection = st.sidebar.button("Start Detection")

    if start_detection:
        rtsp_url = f'rtsp://{username}:{password}@{ip_address}'
        connection_status = st.empty()
        connection_status.write("Connecting to camera...")

        video_placeholder = st.empty()
        if selected_camera == "Parking Road":
            try:
                for frame in number_plate_detection(rtsp_url):
                    connection_status.write("Connected")
                    video_placeholder.image(frame, channels="BGR")
            except Exception as e:
                connection_status.write("Stopped")
                st.error(f"Error: {e}")
        else:
            try:
                for frame in video_detection(rtsp_url):
                    connection_status.write("Connected")
                    video_placeholder.image(frame, channels="BGR")
            except Exception as e:
                connection_status.write("Stopped")
                st.error(f"Error: {e}")



# def main():
#     st.title("Real-Time PPE Detection")

#     st.sidebar.header("Camera Configuration")
#     username = st.sidebar.text_input("Username", value="Test")
#     password = st.sidebar.text_input("Password", value="Admin@123", type="password")
#     camera_options = {
#         "Store": "172.27.4.28",
#         "Main Gate": "172.27.4.35",
#         "Parking Road": "172.27.4.210",
#         "Safety Check": "172.27.4.136"
#     }
#     selected_cameras = st.sidebar.multiselect("Select Cameras", options=list(camera_options.keys()))
#     start_detection = st.sidebar.button("Start Detection")

#     if start_detection and selected_cameras:
#         rtsp_urls = {camera_name: f'rtsp://{username}:{password}@{camera_options[camera_name]}' for camera_name in selected_cameras}

#         # Create columns for each camera
#         cols = st.columns(len(rtsp_urls))

#         for i, (camera_name, rtsp_url) in enumerate(rtsp_urls.items()):
#             with cols[i]:
#                 connection_status = st.info(f"Connecting to {camera_name}...")
#                 video_placeholder = st.empty()
#                 try:
#                     for frame in number_plate_detection(rtsp_url):
#                         connection_status.info("Connected")
#                         video_placeholder.image(frame, channels="BGR")
#                 except Exception as e:
#                     connection_status.error(f"Error: {e}")
#                     st.error(f"Error: {e}")


if __name__ == "__main__":
    main()