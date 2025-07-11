from PIL import Image
import numpy as np
from numpy import asarray

input_image=Image.open("calib-0018_0.tif").convert("L")
input_image_array=asarray(input_image)
image_width, image_height = input_image.size
group_size=6
group_array4D=np.zeros([int(image_height/group_size), int(image_width/group_size), group_size, group_size], dtype=np.uint8)
group_array3D=np.zeros([int(image_height/group_size), int(image_width/group_size), group_size**2], dtype=np.uint8)
binned_image_array=np.zeros((int(image_height/group_size), int(image_width/group_size)))

for i in range(int(image_height/group_size)):
    for j in range(int(image_width/group_size)):
        bin_sum=0
        for k in range(group_size):
            for l in range(group_size):
                bin_sum+=int(input_image_array[group_size*i+k][group_size*j+l])
        binned_image_array[i][j]=bin_sum/group_size**2
            
binned_image=Image.fromarray(binned_image_array)
input_image.show()
binned_image.show()