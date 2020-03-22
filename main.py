import cv2

cap = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")
rect_color = (255,0,0)
while True:
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=2)
    for (x,y,w,h) in faces:
        print(x,y,w,h)
        cv2.rectangle(frame, (x,y), (x+w, y+h), rect_color, 2)

    cv2.imshow("webcam", frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()