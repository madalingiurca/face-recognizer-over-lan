import pickle
from socket import socket, SOCK_STREAM, AF_INET, error

import cv2
import numpy


class Server:
    """clasa folosita de GUI pentru a gestiona functionarea serverului
    coduri erori 1-__init__() exeption
                 2-listen() exception"""

    def __init__(self, host, port):
        """pretty obvious
        AF_INET - IPv4 / AF_INET6 - IPv6
        SOCK_STREAM - TCP SOCKET
        SOCK_DGRAM - UPD SOCKET ||| pick a side"""
        self.host: str = host
        self.port: int = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.clients = {}
        self.clientsNo = 0
        self.faceTags = {}
        try:
            self.faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_alt_tree.xml")
            self.ai = cv2.face.LBPHFaceRecognizer_create()
        except Exception as e:
            print(e)
            exit(1)

    def load_resources(self):
        """incarca dictionarul ce asociaza label-ul cu numele
            dictionarul a fost serializat intr-un fisier .rick folosind pickle
            incarca si modelul Local Binary Pattern Histogram antrenat deja"""
        self.ai.read("Resources/face_trainer.yml")
        with open("Resources/faces.rick", 'rb') as f:
            dump = pickle.load(f)  # type: dict
            self.faceTags = {v: k for k, v in dump.items()}

    def start(self):
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(10)  # 10 unnaccepted connections until they are refused
        except error as err:
            print(err)
            exit(2)

    def stop(self):
        # for t in self.threads: # type: Thread
        #     t.join()
        self.sock.close()

    @staticmethod
    def recvall(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def detect_face(self, imag):
        """functia proceseaza o imagine
        extrage fata + asocierea unui tag"""
        imag = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)  # convert RGB->GrayScale
        faces = self.faceCascade.detectMultiScale(imag)
        persons = {}
        for (x, y, w, h) in faces:
            # extract region/regions of interest
            roi = imag[y:y + h, x:x + w]
            label, conf = self.ai.predict(roi)  # label + confidence
            if conf < 50:
                persons[label] = 1
            else:
                persons[label] = 0
        if not persons:
            return None

        return persons

    def handler(self, conn, addr):
        self.clients[addr] = 1
        try:
            length = int.from_bytes(conn.recv(16), 'big')  # se primeste numarul de biti ce urmeaza a fi primiti
            stringData = self.recvall(conn, int(length))
            if stringData == b'':
                print("User ", addr[0], ":", addr[1], " disconnected!")

            encodedimage = numpy.fromstring(stringData, dtype='uint8')
            decimg = cv2.imdecode(encodedimage, 1)

            persons = self.detect_face(decimg)
            if not persons:
                return "No face detected"
            for key in persons:
                if persons[key] == 1:
                    return self.faceTags[key]
                else:
                    return "Unknown"
            cv2.waitKey(1000)
        except Exception as e:
            print(e)
            print("Disconnected!")
            cv2.destroyAllWindows()
            return 0
