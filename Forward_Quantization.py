from scipy.fft import dct
import numpy as np
import RLC as rlc

class Forward_Quantization:
    def __init__(self,Y,Cb,Cr,level,type):
        self.Y=Y
        self.Cb=Cb
        self.Cr=Cr
        self.level=level
        self.type=type
        
    def macroBlock(image):
        #Convert the layers to 8*8 macro block
        height, width = image.shape
        macroblocks_height = height // 8
        macroblocks_width = width // 8
        macroblocks = np.zeros((macroblocks_height, macroblocks_width, 8, 8))
        for y in range(macroblocks_height):
            for x in range(macroblocks_width):
                macroblocks[y, x] = image[y*8:(y+1)*8, x*8:(x+1)*8]
        return macroblocks
    
    def DCT(macro_image,flag,level,f):
        #apply DCT
        macroblocks_height,macroblocks_width,_,_=macro_image.shape
        for i in range(macroblocks_height):
            for j in range(macroblocks_width):
                dct_img=dct(dct(macro_image[i][j].T,norm='ortho').T,norm='ortho')
                dct_img_Q=Forward_Quantization.qunatize(dct_img,level,flag) #do the qunatization to the macro block
                RunLength=rlc.RLC_ZigZag(dct_img_Q,f) #Apply zigzag and Run length coding and save it in a text file
                RunLength.zigzag()
        return

    def qunatize(macroblocks_dct,level,flag):
        #Qunatization Matrix for Luma
        quantization_matrix_Y = np.array([
                [16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]
            ])
        #Qunatization Matrix for Chroma
        quantization_matrix_CbCr = np.array([
                [17, 18, 24, 47, 99, 99, 99, 99],
                [18, 21, 26, 66, 99, 99, 99, 99],
                [24, 26, 56, 99, 99, 99, 99, 99],
                [47, 66, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99]
            ])
        if(flag=="Y"):
            #apply the qunatiztion to the Luma Layer
            #quantization_matrix_Y = np.around(np.clip(quantization_matrix_Y*level, 0, 255))
            quantization_matrix_Y = np.around((quantization_matrix_Y*level))
            quantized_blocks = np.around(macroblocks_dct/(quantization_matrix_Y))
            #quantized_blocks = np.around(macroblocks_dct/(1))
            
        elif(flag=="CbCr"):
            #apply the qunatiztion to the Chroma Layer
            #quantization_matrix_CbCr = np.around(np.clip(quantization_matrix_CbCr*level, 0, 255))
            quantization_matrix_CbCr = np.around((quantization_matrix_CbCr*level))
            quantized_blocks = np.around(macroblocks_dct/(quantization_matrix_CbCr))
            #quantized_blocks = np.around(macroblocks_dct/(1))
        
        return quantized_blocks

    def Forward_Quantization(self):
        level=self.level
        height,width=self.Y.shape
        #Header of the text file
        info="height: "+str(height)+" Width: "+str(width)+" Levels: "+str(level)+" Block: "+str(8)
        #I=Image
        #V=Video
        if(self.type=="I"):
            f = open("Compress.txt", "a")
        elif(self.type=="V"):
            f = open("Video Compress.txt", "a")
        f.write(info)
        f.write('\n')
        
        Y_macro_image=Forward_Quantization.macroBlock(self.Y)
        Cb_macro_image=Forward_Quantization.macroBlock(self.Cb)
        Cr_macro_image=Forward_Quantization.macroBlock(self.Cr)
        Y_DCT_image=Forward_Quantization.DCT(Y_macro_image,"Y",level,f)
        Cb_DCT_image=Forward_Quantization.DCT(Cb_macro_image,"CbCr",level,f)
        Cr_DCT_image=Forward_Quantization.DCT(Cr_macro_image,"CbCr",level,f)
        print("Compression Completed!")
        f.close()
        return
    