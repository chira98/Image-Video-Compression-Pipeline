import numpy as np
import Inverse_Quantization as InverseQ
import cv2
import unblock
from PIL import Image

def main():
    with open('Compress.txt', 'r') as file:
        #Read the Compress txt irst line
        #extract the information from Header
        first_line = file.readline().split()
        first_n=len(first_line)
        info=[]
        for i in range(first_n):
            if(i%2 != 0):
                info.append((first_line[i]))

        height,width,level,block_size=int(info[0]),int(info[1]),float(info[2]),int(info[3])
        macroblocks_height = height // block_size
        macroblocks_width = width // block_size
        #define the matrix to add the Y,Cb,Cr reconstructed macro block
        matrix = np.zeros((macroblocks_height,macroblocks_width,3,block_size,block_size))
        matrix_row=0
        matrix_col=0
        channel=0

        for line in file:
            #read the file line by line
            values = line.split()
            n=len(values)
            #block is define for macro block
            block = np.zeros((8, 8))
            #Apply inverse zigzag and RLC
            row = 0
            col = 0
            direction = 1
            for i in range(n):
                if(i%2==0):
                    count=int(values[i+1])
                    value=int(values[i])  
                    #inverse zig-zag Transformation
                    while (count > 0):
                        block[row][col] = (value) #assign the values to maco block
                        if direction == 1: 
                            if col == 7:
                                row += 1
                                direction = -1
                            elif row == 0:
                                col += 1
                                direction = -1
                            else:
                                row -= 1
                                col += 1
                        else:  
                            if row == 7:
                                col += 1
                                direction = 1
                            elif col == 0:
                                row += 1
                                direction = 1
                            else:
                                row += 1
                                col -= 1
                        count=count-1
            #print(block)
            #apply Dequnatization and Inverse DCT
            I_Q=InverseQ.Inverse_Quantization(block,channel,level)       
            block=I_Q.IQ()
            #Assign the macro block to the corresponding layer
            matrix[matrix_row][matrix_col][channel] = block
            matrix_col=matrix_col+1
            if(matrix_col>=macroblocks_width):
                matrix_row=matrix_row+1
                matrix_col=0
            if(matrix_row>=macroblocks_height):
                channel=channel+1 #check for the Y,Cb,Cr layer
                matrix_row=0
                matrix_col=0
                if(channel>=3):
                    break

    #remove the 8*8 blocks and creat a full layer
    UnblockMatrix=unblock.Unblock(matrix)
    YCbCr=UnblockMatrix.unblock()
    YCbCr = np.clip(YCbCr, 0, 255).astype(np.uint8) #clip some values to 255
    rgb = cv2.cvtColor(YCbCr, cv2.COLOR_YCrCb2BGR) #convert back to RGB
    image_pil = Image.fromarray(rgb)
    image_pil.save('Compressed Image.jpg')   #save the image
    print("Decompression Completed") 

if __name__ == "__main__":
    main()
        
         
    

       