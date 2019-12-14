from socket import *
import threading
import sys

clients = {}
server_is_closed = False


def send(sock, addr):
    while sock in clients:
        try:
            print('To. ip: ', str(addr))
            send_data = input('>>>')
            sock.send(send_data.encode('utf-8'))
        except (KeyboardInterrupt, SystemExit):
            sock.close()
            sys.exit()


def receive(sock, addr):
    while sock in clients:
        try:
            recv_data = sock.recv(1024)
            recv_data = recv_data.decode('utf-8')
            if recv_data == 'exit':
                print('상대방({}) 이 나갔습니다 : {}'.format(str(addr), recv_data))
                del clients[sock]
                break
            print('상대방({}) : {}'.format(str(addr), recv_data))
        except (KeyboardInterrupt, SystemExit):
            sock.close()
            sys.exit()


def accept_client(server_sock):
    while server_is_closed is not True:
        try:
            server_sock.listen(1)
            conn_sock, addr = server_sock.accept()
            clients[conn_sock] = addr
            print('{} 번째 Client가 {} 에서 접속되었습니다.'.format(len(clients), str(addr)))
            sender = threading.Thread(target=send, args=(conn_sock, addr,))
            receiver = threading.Thread(target=receive, args=(conn_sock, addr,))

            sender.start()
            receiver.start()
        except (KeyboardInterrupt, SystemExit):
            server_sock.close()
            sys.exit()


def main():
    server_sock = None
    try:
        port = 8080

        server_sock = socket(AF_INET, SOCK_STREAM)
        server_sock.bind(('', port))

        print('%d번 포트로 접속 대기중...' % port)
        accepter = threading.Thread(target=accept_client, args=(server_sock,))
        accepter.start()
        accepter.join()

    except (KeyboardInterrupt, SystemExit):
        server_sock.close()
        sys.exit()


if __name__ == "__main__":
    main()
