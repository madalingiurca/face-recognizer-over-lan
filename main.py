import cv2

cap = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

while True:
    ret, frame = cap.read()

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("webcam", frame)
    faces = faceCascade.detectMultiScale(grayFrame, scaleFactor=1.3, minNeighbors=2)


    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()