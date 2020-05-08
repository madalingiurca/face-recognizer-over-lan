import socket
import cv2
import numpy
import argparse

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

parser=argparse.ArgumentParser(description='host, port')
parser.add_argument('host', type=str)
parser.add_argument('port', type=int)
args=parser.parse_args()
#s.connect(('localhost', 8888))
s.connect((args.host, args.port))

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    # codarea imaginii pentru a fi trimisa
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    s.send(len(stringData).to_bytes(16, 'big'))
    s.send(stringData)

    cv2.imshow("Client", frame)
    if cv2.waitKey(500) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

s.close()
