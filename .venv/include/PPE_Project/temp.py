import cv2 
def main():
    rtsp_url1 = 'rtsp://Test:Admin@123@172.27.4.35'  
    rtsp_url2 = 'rtsp://Test:Admin@123@172.27.4.136'  
    
    # show both video streams side by side without streamlit
    cap1 = cv2.VideoCapture(rtsp_url1)
    cap2 = cv2.VideoCapture(rtsp_url2)
    while True:
        success1, img1 = cap1.read()
        success2, img2 = cap2.read()
        if not success1 or not success2:
            print("Failed to access the camera.")
            break
        img1_resized = cv2.resize(img1, (640, 480))
        img2_resized = cv2.resize(img2, (640, 480))
        cv2.imshow("Camera 1", img1_resized)
        cv2.imshow("Camera 2", img2_resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

main()