from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import struct



class VideoServer:

    def __init__(self,):
        self.HOST = ''
        self.PORT = 3000
        self.lnF = 640*480*3
        self.CHUNK = 1024
        self.addresses = {}
        self.threads = {}
        self.server = socket(family=AF_INET, type=SOCK_STREAM)
        try:
            self.server.bind((self.HOST, self.PORT))
        except OSError:
            print("Servidor Ocupado")
        self.server.listen(2)
        self.accept_thread = Thread(target=self.connections)
        self.accept_thread.start()
        self.accept_thread.join()
        self.server.close()

    def connections(self,):
        while True:
            try:
                client , address = self.server.accept()
                self.addresses[client] = address
                if len(self.addresses) > 1:
                    for socket in self.addresses:
                        if socket not in self.threads:
                            self.threads[socket] = True
                            socket.send(('start').encode())
                            Thread(target=self.client_connection, args=(socket, )).start()
                else:
                    continue
            except Exception as e:
                continue

    def client_connection(self, client):
        while True:
            try:
                length_buff = self.recvall(client=client, buffer_size=4)
                length,  = struct.unpack('!I', length_buff)
                self.recvall(client=client, buffer_size= length) 
            except Exception as e:
                continue

    def broad_cast(self, client_socket, data_to_be_sent):
        for client in self.addresses:
            if client != client_socket:
                client.sendall(data_to_be_sent)

    def recvall(self, client, buffer_size):
        data_bytes = b''
        i = 0
        while i != buffer_size:
            to_read = buffer_size - i
            if to_read > ( self.CHUNK * 1000):
                data_bytes = client.recv(self.CHUNK * 1000)
                i += len(data_bytes)
                self.broad_cast(client_socket=client, data_to_be_sent= data_bytes)
            else:
                if buffer_size == 4:
                    data_bytes += client.recv(to_read)
                else:
                    data_bytes = client.recv(to_read)
            i += len(data_bytes)
            if buffer_size != 4:
                self.broad_cast(client_socket=client, data_to_be_sent= data_bytes)

        if buffer_size == 4:
            self.broad_cast(client_socket=client, data_to_be_sent= data_bytes)
            return data_bytes


x = VideoServer()