from server import Server

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread



  
class AudioServer(Server):

    def __init__(self) -> None:
        super().__init__()
        self.HOST = ''
        self.PORT = 4000
        self.buffer_size = 4096
        self.addresses = {}
        self.server = socket(family=AF_INET, type=SOCK_STREAM)
        try:
            self.server.bind((self.HOST, self.PORT))
        except OSError:
            print("Servidor Ocupado")

        self.server.listen(2)
        self.accept_thread = Thread(target=self.connections)
        self.accept_thread.start()
        self.accept_thread.join()

    def connections(self,):
        while True:
            try:
                client, address = self.serve.accept()
                self.addresses[client] = address
                Thread(target=self.client_connection, args=(client, )).start()
            except Exception as e:
                continue


    def client_connection(self, client):
        while True:
            try:
                data = client.recv(self.buffer_size)
                self.broad_cast(
                    client_socket= client, 
                    data_to_be_sent= data
                )
            except Exception as e:
                continue


    def broad_cast(self, client_socket, data_to_be_sent):
        for client in self.addresses:
            if client != client_socket:
                client.sendall(data_to_be_sent)
    

