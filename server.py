from socket import *
from threading import *

from PyQt5.QtCore import pyqtSignal, QObject

import time


class Signal(QObject):
    conn_signal = pyqtSignal()
    recv_signal = pyqtSignal(str)


class ServerSocket:

    def __init__(self, parent):
        self.parent = parent
        self.bListen = False
        self.clients = []
        self.ip = []
        self.threads = []

        self.conn = Signal()
        self.recv = Signal()

        self.conn.conn_signal.connect(self.parent.updateClient)
        self.recv.recv_signal.connect(self.parent.updateMsg)
        self.heart_beat_ack = False

    def __del__(self):
        self.stop()

    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)

        try:
            self.server.bind((ip, port))
        except Exception as e:
            print('Bind Error : ', e)
            return False
        else:
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,))
            self.t.start()
            print('Server Listening...')

        return True

    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('Server Stop')

    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error : ', e)
                break
            else:
                item = {'client': client, 'hb': True, 'addr': addr}
                self.clients.append(item)
                self.ip.append(addr)
                self.conn.conn_signal.emit()
                t = Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()

                heart_beat_t = Thread(target=self.heart_beat_send, args=(item,))
                self.threads.append(heart_beat_t)
                heart_beat_t.start()

        self.remove_all_clients()
        self.server.close()

    def receive(self, addr, client):
        while True:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = str(recv, encoding='utf-8')
                if msg and msg != 'HEART_BEAT_ACK':
                    self.send(msg)
                    self.recv.recv_signal.emit(msg)
                    print('[RECV]:', addr, msg)
                    if msg == "exit":
                        break
                elif msg and msg == 'HEART_BEAT_ACK':
                    for c in self.clients:
                        if c['client'] is client:
                            c['hb'] = True
                            print('heart_beat_ack incoming')

        self.remove_client(addr, client)

    def send(self, msg):
        try:
            for c in self.clients:
                c['client'].send(msg.encode())
        except Exception as e:
            print('Send() Error : ', e)

    def heart_beat_send(self, c):
        while True:
            try:
                if c['hb'] is not True:
                    print('client connection anomaly detected')
                    break
                else:
                    c['hb'] = False
                    c['client'].send('HEART_BEAT'.encode())
            except Exception as e:
                print('HEART_BEAT Error : ', e)
                break
            else:
                time.sleep(1)

        self.remove_client(c['addr'], c['client'])

    def remove_client(self, addr, client):
        client.close()
        if addr in self.ip:
            self.ip.remove(addr)
        for c in self.clients:
            if c['client'] is client and c in self.clients:
                self.clients.remove(c)
        # self.clients.remove(client)

        self.conn.conn_signal.emit()
        print('remove client')

        i = 0
        for t in self.threads[:]:
            if not t.isAlive():
                del (self.threads[i])
            i += 1

        self.resource_info()

    def remove_all_clients(self):
        for c in self.clients:
            c['client'].close()

        self.ip.clear()
        self.clients.clear()
        self.threads.clear()

        self.conn.conn_signal.emit()

        self.resource_info()

    def resource_info(self):
        print('Number of Client ip\t: ', len(self.ip))
        print('Number of Client socket\t: ', len(self.clients))
        print('Number of Client thread\t: ', len(self.threads))
