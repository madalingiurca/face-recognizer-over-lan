from socket import *
from threading import *

import cv2  # pentru debug/vizualizarea imaginilor primite pe server
import numpy

import server_utils


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


HOST = ''
PORT = 8888
clients_list = {}
s = socket(AF_INET, SOCK_STREAM)
client_no = 0

try:
    s.bind((HOST, PORT))
except error as e:
    print(e)
    exit(1)

s.listen(10)
print('Socket listening')

face_tag = server_utils.load_resources()


def analyze(conn, addr):
    clients_list[addr] = 1
    while True:
        try:
            length = int.from_bytes(conn.recv(16), 'big')  # se primeste numarul de biti ce urmeaza a fi primiti
            stringData = recvall(conn, int(length))
            encodedimage = numpy.fromstring(stringData, dtype='uint8')
            decimg = cv2.imdecode(encodedimage, 1)

            cv2.imshow("Server", decimg)
            persons = server_utils.detect_face(decimg)
            if not persons:
                print("No face detected")
                continue
            for key in persons:
                if persons[key] == 1:
                    print(face_tag[key])
                else:
                    print("Unknown")

            cv2.waitKey(1000)
        except Exception as e:
            print(e)
            print("Disconnected!")
            cv2.destroyAllWindows()
            break


while True:
    conn, addr = s.accept()
    print("Connected with " + str(addr[0]) + ':' + str(addr[1]))
    t = Thread(target=analyze, args=(conn, addr))
    t.start()
