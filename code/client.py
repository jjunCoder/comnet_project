from socket import *
import threading
import sys
from signal import *

THREADS = []
client_sock = None


def handler(signal, frame):
    global THREADS
    global client_sock
    print('key exit')
    send_data = 'exit'
    client_sock.send(send_data.encode('utf-8'))
    client_sock.close()
    for t in THREADS:
        t.join(1)
    sys.exit()


def send(sock):
    while True:
        send_data = input('>>>')
        sock.send(send_data.encode('utf-8'))


def receive(sock):
    while True:
        recv_data = sock.recv(1024)
        print('상대방 :', recv_data.decode('utf-8'))


def main():
    server_ip = '127.0.0.1'
    # server_ip = '165.132.5.144'
    global client_sock

    port = 8080

    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect((server_ip, port))

    print('접속 완료')

    sender = threading.Thread(target=send, args=(client_sock,))
    receiver = threading.Thread(target=receive, args=(client_sock,))

    sender.start()
    THREADS.append(sender)
    receiver.start()
    THREADS.append(receiver)

if __name__ == "__main__":
    signal(SIGINT, handler)
    main()

