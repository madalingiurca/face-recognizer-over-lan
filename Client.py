import socket
import cv2
import numpy

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8888))

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    #print("frame = " + str(len(frame)))

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
