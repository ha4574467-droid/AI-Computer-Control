import cv2
import math
import time
import pyautogui
import mediapipe as mp

# Screen resolution get karein
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='models/hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO
)

cap = cv2.VideoCapture(0)

# Smoothing factors
prev_x, prev_y = 0, 0
smooth_factor = 5

with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        frame_timestamp_ms = int(time.time() * 1000)
        result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                thumb_tip = hand_landmarks[4]
                index_tip = hand_landmarks[8]

                # Map camera coordinates to full screen size
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

                target_x = int(index_tip.x * screen_w)
                target_y = int(index_tip.y * screen_h)

                # Cursor Movement Smoothing Logic
                curr_x = prev_x + (target_x - prev_x) / smooth_factor
                curr_y = prev_y + (target_y - prev_y) / smooth_factor
                
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

                # Distance between Thumb and Index for Click
                distance = math.hypot(tx - ix, ty - iy)

                if distance < 30:
                    pyautogui.click()
                    cv2.putText(frame, "ACTION: CLICK!", (20, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    cv2.line(frame, (ix, iy), (tx, ty), (0, 0, 255), 3)

        cv2.imshow("AI Gesture Mouse Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()