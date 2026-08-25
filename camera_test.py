import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera open nahi ho raha!")
    exit()

print("Camera successfully connected!")
print("Camera band karne ke liye Q press karein.")

while True:
    success, frame = camera.read()

    if not success:
        print("Camera se frame nahi mil raha!")
        break

    cv2.imshow("AI Computer Control - Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()