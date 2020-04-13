from socket import *
from threading import *

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


def thread_comm(conn, addr):
    clients_list[addr] = 1
    while True:
        msg = conn.recv(1024).decode('ascii')
        if msg == '{quit}' or not msg:
            print(addr, "DISCONNECTED")
            conn.send(bytes("Disconnected!", 'ascii'))
            conn.close()
            break
        print(addr, msg)


while True:
    conn, addr = s.accept()
    print("Connected with " + str(addr[0]) + ':' + str(addr[1]))
    t = Thread(target=thread_comm, args=(conn, addr))
    t.start()