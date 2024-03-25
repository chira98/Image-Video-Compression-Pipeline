from skimage import color, io
import numpy as np
import cv2
import matplotlib.pyplot as plt

class YCbCr:
    def __init__(self,image):
        self.image=image

    def convert(self):
        #convert RGB to YCbCr
        ycbcr = cv2.cvtColor(self.image, cv2.COLOR_BGR2YCrCb)
        Y = ycbcr[:, :, 0]
        Cb = ycbcr[:, :, 1]
        Cr = ycbcr[:, :, 2]
        return Y,Cb,Cr
