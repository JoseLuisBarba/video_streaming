import cv2
import numpy as np
from typing import Any, Tuple, List
import zlib

class TransformPipeline:
    def __init__(self, functions: List) -> None:
        self.functions = functions

    def transform(self, x):
        for fun in self.functions:
            x = fun(x)
        return x




def to_rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def to_resize(frame, new_shape: Tuple= (640, 480)):
    return cv2.resize(frame, new_shape)

def to_tensor(frame, longFrame: int):
    return np.array(frame, dtype=np.uint8).reshape(1, longFrame)

def to_bytearray(frame):
    return bytearray(frame) #jpg

def to_compress(frame):
    return zlib.compress(frame, compresslevel=9)

class FramePipeline:    
    def __call__(self, frame):
        self.functions = [to_rgb, to_resize, to_tensor, to_bytearray, to_compress]
        self.trans_pipe = TransformPipeline(functions=self.functions)
        return self.trans_pipe.transform(frame)

