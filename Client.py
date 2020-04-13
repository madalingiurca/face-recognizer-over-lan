from recognizer import start_reco
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8888))

start_reco(s)

s.close()