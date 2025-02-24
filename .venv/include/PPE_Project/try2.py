import cv2
from ultralytics import YOLO
import easyocr
import streamlit as st
import numpy as np
from threading import Thread
from multiprocessing import Process, Manager

def capture_video(camera_id, queue):
    cap = cv2.VideoCapture(camera_id)
    while True:
        success, img = cap.read()
        if not success:
            print(f"Failed to access camera {camera_id}.")
            break
        queue.append(img)
    cap.release()

def video_detection(camera_id, queue):
    classNames = ['Halmet', 'Mask', 'NO-Halmet', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone',
                  'Safety Vest', 'machinery', 'vehicle']

    model = YOLO("/home/ritik/Documents/second/.venv/include/PPE_Project/YOLO-Weights/ppe.pt").to('cuda')

    while True:
        if len(queue) == 0:
            continue 
        
        img = queue.pop(0)
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

def number_plate_detection(rtsp_url,queue):
    model = YOLO("/home/ritik/Documents/second/.venv/include/PPE_Project/YOLO-Weights/number_plate.pt").to('cuda')  
    reader = easyocr.Reader(['en']) 

    while True:
        if len(queue) == 0:
            continue 

        img = queue.pop(0)
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
    st.title("Real-Time PPE Detection")

    st.sidebar.header("Camera Configuration")
    username = st.sidebar.text_input("Username", value="Test")
    password = st.sidebar.text_input("Password", value="Admin@123", type="password")
    
    camera_options = {
        "Store": "172.27.4.28",
        "Main Gate": "172.27.4.35",
        "Parking Road": "172.27.4.210",
        "Safety Check": "172.27.4.136"
    }

    selected_camera_1 = st.sidebar.selectbox("Select Camera 1", list(camera_options.keys()))
    selected_camera_2 = st.sidebar.selectbox("Select Camera 2", list(camera_options.keys()))

    start_detection = st.sidebar.button("Start Detection")

    camera_1_id = f'rtsp://{username}:{password}@{camera_options[selected_camera_1]}'  
    camera_2_id = f'rtsp://{username}:{password}@{camera_options[selected_camera_2]}'  

        
    if start_detection:

        with Manager() as manager:
            frame_queue_1 = manager.list()
            frame_queue_2 = manager.list()

            capture_process_1 = Process(target=capture_video, args=(camera_1_id, frame_queue_1))
            capture_process_1.start()

            capture_process_2 = Process(target=capture_video, args=(camera_2_id, frame_queue_2))
            capture_process_2.start()

            stframe1 = st.empty()
            stframe2 = st.empty()

            col1, col2 = st.columns([1, 1])



            while True:
                with col1:
                    if frame_queue_1:
                        img_bytes_1 = next(number_plate_detection(camera_1_id, frame_queue_1))
                        img_1 = cv2.imdecode(np.frombuffer(img_bytes_1, np.uint8), cv2.IMREAD_COLOR)
                        stframe1.image(img_1, channels="BGR")
                with col2:

                    if frame_queue_2:
                        img_bytes_2 = next(video_detection(camera_2_id, frame_queue_2))
                        img_2 = cv2.imdecode(np.frombuffer(img_bytes_2, np.uint8), cv2.IMREAD_COLOR)
                        stframe2.image(img_2, channels="BGR")
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            capture_process_1.terminate()
            capture_process_2.terminate()

            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
