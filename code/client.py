from socket import *
import threading
import sys


def send(sock):
    while True:
        try:
            send_data = input('>>>')
            sock.send(send_data.encode('utf-8'))
        except:
            print('key exit')
            send_data = 'exit'
            sock.send(send_data.encode('utf-8'))
            sock.close()
            sys.exit()


def receive(sock):
    while True:
        try:
            recv_data = sock.recv(1024)
            print('상대방 :', recv_data.decode('utf-8'))
        except:
            print('key exit')
            send_data = 'exit'
            sock.send(send_data.encode('utf-8'))
            sock.close()
            sys.exit()


def main():
    server_ip = '127.0.0.1'
    # server_ip = '165.132.5.144'
    client_sock = None

    try:
        port = 8080

        client_sock = socket(AF_INET, SOCK_STREAM)
        client_sock.connect((server_ip, port))

        print('접속 완료')

        sender = threading.Thread(target=send, args=(client_sock,))
        receiver = threading.Thread(target=receive, args=(client_sock,))

        sender.start()
        receiver.start()

    except:
        print('key exit')
        send_data = 'exit'
        client_sock.send(send_data.encode('utf-8'))
        client_sock.close()
        sys.exit()


if __name__ == "__main__":
    main()
