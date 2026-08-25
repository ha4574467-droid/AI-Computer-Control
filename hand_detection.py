import cv2
import mediapipe as mp

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera open nahi ho raha!")
    exit()

print("Hand Detection Started")
print("Q press karke band karein.")

while True:
    success, frame = camera.read()

    if not success:
        print("Camera se frame nahi mil raha!")
        break

    # OpenCV BGR -> RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand detection
    results = hands.process(rgb_frame)

    # Detected hand draw karo
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Landmark coordinates print karna
            for landmark in hand_landmarks.landmark:
                height, width, _ = frame.shape

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                # Har point ka coordinate available hoga
                # print(x, y)

    cv2.imshow("AI Computer Control - Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
hands.close()
cv2.destroyAllWindows()