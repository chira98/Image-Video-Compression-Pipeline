import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
import Ycbcr as conv
import Forward_Quantization as FQ
import Decompress
import os
import math
import cv2
from PIL import Image


def main():
    #image = imread('Image.jpg')
    #read the image
    image = imread('Parrots-680x680.jpg')
    #convert the image to YCbCr
    ycbcr=conv.YCbCr(image)
    Y,Cb,Cr=ycbcr.convert()

    #cv2.imwrite("Y.jpg", Y)
    #cv2.imwrite("Cb.jpg", Cb)
    #cv2.imwrite("Cr.jpg", Cr)
    #clear the file before starting the process
    open('Compress.txt', 'w').close()
    #get the compression qulatiy fom the user
    print("Please enter the desired compression Quality,")
    print("1.High \n2.Medium \n3.Low ")
    levels = int(input("Enter a value: "))
    if(levels==1):
        levels=1
    elif(levels==2):
        levels=3
    elif(levels==3):
        levels=8
    else:
        print("Invalid Input")
    #Start the compression process I=Image
    fq = FQ.Forward_Quantization(Y,Cb,Cr,levels,"I")
    fq.Forward_Quantization()
    #Do the comprression based on the e number

    Y_N = (input("Would you like to determine the compression ratio corresponding to your E number[Y/N]? "))
    if(Y_N=='Y'):
        #ask the user to enter the e number
        e_no = int(input("Please enter your E-Number: "))
        bitrate=e_no+300
        #inialize the value
        Qlevel = 1
        BestQlevel=0
        BestPSNR=0
        while Qlevel <= 50:
            #do the compression task
            open('Compress.txt', 'w').close()
            fq = FQ.Forward_Quantization(Y, Cb, Cr, Qlevel,"I")
            fq.Forward_Quantization()
            #decompression step
            Decompress.main()

            # Read the compressed file size 
            file_size = os.path.getsize('Compress.txt')
            achieved_bit_rate=file_size/1024
           
            Com_image = imread('Compressed Image.jpg')
            #calculate the PSNR Value
            PSNR=psnr(image,Com_image)
            #check whether the conditions are satisfied
            if achieved_bit_rate <= bitrate:
                BestPSNR = PSNR
                BestQlevel = Qlevel
                break
            Qlevel += 1
        print(f"Best quantization level: {BestQlevel}")
        print(f"Best achieved PSNR: {BestPSNR}")

    else:
        print("Process Completed")

  
def psnr(Ori_image, Com_image):
    #calculate the PSNR
    mse = np.mean((Ori_image - Com_image) ** 2)
    psnr = 20 * math.log10(255) - 10 * math.log10(mse)
    return psnr
    

if __name__ == "__main__":
  main()



