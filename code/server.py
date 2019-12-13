from socket import *
import threading
import time

clients = []


def send(sock, addr):
    while True:
        print('To. ip: ', str(addr))
        sendData = input('>>>')
        sock.send(sendData.encode('utf-8'))


def receive(sock, addr):
    while True:
        recvData = sock.recv(1024)
        print('상대방({}) : {}'.format(str(addr), recvData.decode('utf-8')))


def accept_client(server_sock):
    while True:
        connectionSock, addr = serverSock.accept()
        clients.append((connectionSock, addr))
        print('{} 번째 Client가 {} 에서 접속되었습니다.'.format(str(addr), len(clients)))
        sender = threading.Thread(target=send, args=(connectionSock, addr, ))
        receiver = threading.Thread(target=receive, args=(connectionSock, addr, ))

        sender.start()
        receiver.start()


port = 8080

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print('%d번 포트로 접속 대기중...' % port)

accepter = threading.Thread(target=accept_client, args=(serverSock, ))
accepter.start()

while True:
    time.sleep(1)
    pass
