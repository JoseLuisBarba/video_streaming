from client import Client

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import pyaudio
from array import array


class AudioClient(Client):

    def __init__(self) -> None:
        super().__init__()
        self.HOST = ''
        self.PORT = 4000
        self.CHUNK= 1024
        self.CHANNELS=2
        self.RATE= 44100
        self.FORMAT=pyaudio.paInt16
        self.buffer_size = 4096

        self.client = socket(family=AF_INET, type=SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))    
        self.audio=pyaudio.PyAudio()
        self.stream= self.audio.open(
            format= self.FORMAT,
            channels= self.CHANNELS, 
            rate= self.RATE, 
            input= True, 
            output = True,
            frames_per_buffer= self.CHUNK
        )
        self.recieve_audio_thread = Thread(target=self.receive).start()
        self.send_audio_thread = Thread(target=self.send).start()


    def send(self,):
        while True:
            data = self.stream.read(self.CHUNK)
            self.client.sendall(data)

          
    def recieve(self,):
        while True:
            data = self.recvall(self.buffer_size)
            self.stream.write(data)
            
      
    def recvall(self,size):
        data_bytes = b''
        while len(data_bytes) != size:
            to_read = size - len(data_bytes) 
            if to_read > (4 * self.CHUNK):
                databytes += self.client.recv(4 * self.CHUNK)
            else:
               data_bytes += self.client.recv(to_read)
        return data_bytes
