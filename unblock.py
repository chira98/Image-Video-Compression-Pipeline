import numpy as np
class Unblock:
    def __init__(self,matrix):
        self.matrix=matrix

    def unblock(self):
        height, width,channels, _, _ = self.matrix.shape
        image_height = height * 8
        image_width = width * 8
        #remove the 8*8 block
        image = np.zeros((image_height, image_width,channels))
        for j in range(channels):
            for y in range(height):
                for x in range(width):
                    block = self.matrix[y, x, j]
                    image[y*8:(y+1)*8, x*8:(x+1)*8,j] = block

        return image