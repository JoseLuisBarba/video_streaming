from abc import ABC, abstractmethod

class Client:

    @abstractmethod
    def send(self,):
        pass

    @abstractmethod       
    def recieve(self,):
        pass
            
    @abstractmethod   
    def recvall(self,size):
        pass
