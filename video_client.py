from frame_pipeline import FramePipeline
from client import Client

import cv2
from socket import AF_INET, SOCK_STREAM, socket
from imutils.video import WebcamVideoStream
from threading import Thread
import numpy as np
import zlib
import struct


class VideoClient(Client):

    def __init__(self) -> None:
        super().__init__()
        # AF_INET <- familia ipv4
        self.HOST = '192.168.18.5'
        self.PORT = 3000
        self.CHUNK=1024
        self.lnF = 640*480*3 #longitud de fotogramas
        client = socket(family=AF_INET, type=SOCK_STREAM)
        client.connect((self.HOST, self.PORT))
        self.wvs = WebcamVideoStream(0).start()
        self.initiation = client.recv(5).decode()
        if self.initiation == "start":
            self.recieve_frame_thread = Thread(target=self.receive).start()
            self.send_frame_thread = Thread(target=self.send).start()

    def send(self,):
        while True:
            try:
                frame = self.wvs.read()
                data_bytes = FramePipeline()(frame)
                length_data_bytes = struct.pack('!I', len(data_bytes))
                bytes_to_be_send = b''
                self.client.sendall(length_data_bytes)
                while len(data_bytes) > 0:
                    if (1000 * self.CHUNK) <= len(data_bytes):
                        bytes_to_be_send = data_bytes[:(1000 * self.CHUNK)]
                        data_bytes = data_bytes[(1000 * self.CHUNK):]
                        self.client.sendall(bytes_to_be_send)
                    else:
                        bytes_to_be_send = data_bytes
                        self.client.sendall(bytes_to_be_send)
                        data_bytes = b''
            except Exception as e:
                continue


    def recieve(self,):
        while True:
            try:
                lengthbuf = self.recvall(4)
                length, = struct.unpack('!I', lengthbuf)
                databytes = self.recvall(length)
                img = zlib.decompress(databytes)
                if len(databytes) == length:
                    img = np.array(list(img))
                    img = np.array(img, dtype = np.uint8).reshape(480, 640, 3)
                    cv2.imshow("Stream", img)
                    if cv2.waitKey(1) == 27:
                        cv2.destroyAllWindows()
            except Exception as e:
                continue
            

    def recvall(self,size):
        data_bytes = b''
        while(data_bytes) != size:
            to_read = size - len(data_bytes)
            if to_read > (1000 * self.CHUNK):
                data_bytes += self.client.recv(1000 * self.CHUNK)
            else:
                data_bytes += self.client.recv(to_read)
            return data_bytes

     
video = VideoClient()