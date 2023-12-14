from abc import ABC, abstractmethod

 
class Server(ABC):

    @abstractmethod
    def connections(self,):
        pass

    @abstractmethod
    def client_connection(self, client):
        pass

    @abstractmethod
    def broad_cast(self, client_socket, data_to_be_sent):
        pass

    @abstractmethod
    def recvall(self, client, buffer_size):
        pass