import cv2
import math
import time
import os
import threading
import pyautogui
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import mediapipe as mp

screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

last_voice_cmd = "Voice Status: Active"
system_active = True

def voice_listener_thread():
    global last_voice_cmd, system_active
    recognizer = sr.Recognizer()
    sample_rate = 44100
    duration = 3

    while system_active:
        try:
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait()
            wav.write('temp_main.wav', sample_rate, recording)

            with sr.AudioFile('temp_main.wav') as source:
                audio = recognizer.record(source)

            command = recognizer.recognize_google(audio).lower()
            last_voice_cmd = f"Voice: {command}"

            if "open browser" in command or "browser" in command:
                os.system("start msedge")
            elif "notepad" in command:
                os.system("notepad")
            elif "screenshot" in command:
                pyautogui.screenshot("master_screenshot.png")
            elif "volume up" in command:
                pyautogui.press("volumeup", presses=5)
            elif "volume down" in command:
                pyautogui.press("volumedown", presses=5)

        except Exception:
            pass

threading.Thread(target=voice_listener_thread, daemon=True).start()

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='models/hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO
)

cap = cv2.VideoCapture(0)
prev_x, prev_y = 0, 0
smooth_factor = 4

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
            # Multi-hand conflict fix: Sirf Pehle Detected Hand ko pick karein
            hand_landmarks = result.hand_landmarks[0]

            # STRICT LANDMARKS SETUP
            thumb_tip = hand_landmarks[4]    # Thumb Tip ONLY
            index_tip = hand_landmarks[8]    # Index Tip ONLY
            middle_tip = hand_landmarks[12]  # Middle Tip
            wrist = hand_landmarks[0]

            # Convert to camera frame coordinates
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # Strict Pointing Check: Index finger MUST be raised higher than middle finger & wrist
            is_pointing = (index_tip.y < hand_landmarks[6].y) and (middle_tip.y > hand_landmarks[10].y)

            # Highlighting Cursor Point (RED CIRCLE) on INDEX FINGER TIP
            cv2.circle(frame, (ix, iy), 10, (0, 0, 255), -1)

            # Cursor Movement execution ONLY via Index Finger Pointing
            if is_pointing:
                target_x = int(index_tip.x * screen_w)
                target_y = int(index_tip.y * screen_h)

                curr_x = prev_x + (target_x - prev_x) / smooth_factor
                curr_y = prev_y + (target_y - prev_y) / smooth_factor
                
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

            # Pinch / Click Detection (Distance between Thumb Tip #4 and Index Tip #8)
            pinch_distance = math.hypot(tx - ix, ty - iy)
            if pinch_distance < 30:
                pyautogui.click()
                cv2.circle(frame, (ix, iy), 15, (0, 255, 0), -1)
                cv2.line(frame, (ix, iy), (tx, ty), (0, 255, 0), 3)

        cv2.putText(frame, last_voice_cmd, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("AI Computer Control - Strict Finger Engine", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            system_active = False
            break

cap.release()
cv2.destroyAllWindows()
if os.path.exists("temp_main.wav"):
    os.remove("temp_main.wav")