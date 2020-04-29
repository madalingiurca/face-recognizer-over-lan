import pickle
import cv2


#prima implementare
def start_reco(s):
    cap = cv2.VideoCapture(0)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")
    rect_color = (255,0,0)
    ai = cv2.face.LBPHFaceRecognizer_create()
    ai.read("face_trainer.yml")

    with open("faces.rick", 'rb') as f:
        dump = pickle.load(f) #type: dict
        face_name = {v:k for k, v in dump.items()}

    print(face_name)
    while True:
        ret, frame = cap.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(grayFrame, minNeighbors=3, scaleFactor=1.3)

        for (x,y,w,h) in faces:
            #print(x,y,w,h)
            predict_face = grayFrame[y:y+h, x:x+w]
            #cv2.imshow("predict face", predict_face)
            cv2.rectangle(frame, (x,y), (x+w, y+h), rect_color, 2)
            name, conf = ai.predict(predict_face)

            if conf < 70:
                print(x,y,w,h,"conf = ",conf, "person = ", face_name[name])
                msg = conf.__str__() + " " + face_name[name]
                s.send(bytes(msg, 'ascii'))
            else:
                print("unknown with conf = ", conf)
                msg = "unknown with conf = " + conf.__str__()
                s.send(bytes(msg, 'ascii'))
        cv2.imshow("webcam", frame)
        if cv2.waitKey(600) & 0xFF == ord('q'):
            msg = "{quit}"
            s.send(bytes(msg, 'ascii'))
            break
    cap.release()
    cv2.destroyAllWindows()