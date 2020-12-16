import cv2
import os

class Video:
    def __init__(self, path):
        #test path exists
        try:
            self._handler = cv2.VideoCapture(path)
        except:
            raise Exception('Path does not exist')
            #Something to destroy the function here
        self.path = path
        self.current_frame = 0

    def __iter__(self):
        self.current_frame = 0
        return self
    #I think that above doesn't do anythin
    def __next__(self):
        r, self._frame = self._handler.read()
        self.frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
        self.current_frame +=1
        if r == False:
            raise StopIteration
        else:
            return self.frame

    def getDimensions(self):
        return (self.frame.shape) #form x, y

    def __del__(self):
        self._handler.release()
