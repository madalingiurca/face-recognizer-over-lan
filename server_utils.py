import pickle
import cv2


faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_alt_tree.xml")
ai = cv2.face.LBPHFaceRecognizer_create()
ai.read("Resources/face_trainer.yml")
def load_resources():
    """incarca dictionarul ce asociaza label-ul cu numele
        dictionarul a fost serializat intr-un fisier .rick folosind pickle"""
    with open("Resources/faces.rick", 'rb') as f:
        dump = pickle.load(f)  # type: dict
        face_tag = {v: k for k, v in dump.items()}
    ai.read("Resources/face_trainer.yml")
    return face_tag


def detect_face(imag):
    """functia proceseaza o imagine
    extrage fata + asocierea unui tag"""
    imag = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY) #convert RGB->GrayScale
    faces = faceCascade.detectMultiScale(imag)
    persons = []
    for (x, y, w, h) in faces:
        #extract region/regions of interest
        roi = imag[y:y+h, x:x+w]
        label, conf = ai.predict(roi) #label + confidence
        if conf < 70:
            persons.append(label)
    return persons