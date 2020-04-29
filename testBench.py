from ServerClass import Server
from threading import Thread
serv = Server('', 8888)
serv.load_resources()

T = Thread(target=serv.start)
T.start()
