#from IPython import get_ipython
#get_ipython().magic('reset -sf')

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from numpy import asarray
import math
from scipy.interpolate import CloughTocher2DInterpolator
from scipy.spatial import KDTree, Delaunay
import csv
import shapely
import os

#create folder to store images within environment
folder_path="synthImages"
try:
    os.mkdir(folder_path)
    print(f"Folder '{folder_path}' created successfully.")
except FileExistsError:
    print(f"Folder '{folder_path}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

"""CSV LOADING FROM FE MODEL"""
#load image with defined mm/pixel scale
speckle_image_path="calib-0018_0.tif"
speckle_image=Image.open(speckle_image_path).convert("L")
image_array=asarray(speckle_image)
image_width,image_height = speckle_image.size
scale=0.042857
#scale=0.2575

#take csv generated from ABAQUS script and convert to list of each line in csv
row_list=[]
with open("plasticdeformationFULL.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        row_list.append(row[0].split(','))

#find number of steps in FE model
steps=1
    
#find number of nodes in FE mesh        
num_nodes=int((len(row_list)-1)/steps)

#find location of FE nodes in millimeters and convert to pixel locations
undeformed_nodes_mm=[]
undeformed_nodes_px=[]
surface_node_list=[]
timeIncrements=[]
for row in row_list:
    try:
        if float(row[4])==0:
            if row[0]=='0.0':
                undeformed_nodes_mm.append([float(row[2]),float(row[3]),float(row[4])])
                undeformed_nodes_px.append([float(row[2])/scale,float(row[3])/scale])
            #store node locations where z=0
            surface_node_list.append(row)
        else:
            continue
        if float(row[0]) not in timeIncrements:
            timeIncrements.append(float(row[0]))
    except ValueError:
        continue

#find displacements at each node in millimeters and convert to pixel units    
displacement_mm=np.zeros([len(timeIncrements),len(undeformed_nodes_mm), 3])
displacement_px=np.zeros([len(timeIncrements),len(undeformed_nodes_mm), 2])
for i in range(len(timeIncrements)):
    for j in range(len(undeformed_nodes_mm)):
        displacement_mm[i][j]=[float(surface_node_list[i*len(undeformed_nodes_mm)+j][5]),
                               float(surface_node_list[i*len(undeformed_nodes_mm)+j][6]), 
                               float(surface_node_list[i*len(undeformed_nodes_mm)+j][7])]
        displacement_px[i][j]=[float(surface_node_list[i*len(undeformed_nodes_mm)+j][5])/scale,
                               float(surface_node_list[i*len(undeformed_nodes_mm)+j][6])/scale]

'''
#View nodes imposed onto undeformed image
buffer = np.zeros([image_height, image_width, 4], dtype=np.uint8)
for node in undeformed_nodes_px:
    if 0<node[0]<image_width and 0<node[1]<image_height:
        buffer[int(node[1]),int(node[0])]=[255,0,0,255]
undeformed_mesh = Image.fromarray(buffer, "RGBA") # Convert buffer to image
background = Image.open(speckle_image_path).convert("RGBA") # Load background speckle image
image_overlay = Image.alpha_composite(background, undeformed_mesh) # Overlay images
image_overlay.show() # Show final image
'''

UndeformedImageArray=np.array(image_array)
"""IMAGE DEFORMATION ALGORITHM"""    
for i in range(68,len(timeIncrements)):
    RasterDeformedPixelList=[]
    GreyvalueList=[]
    RasterNodeDisplacementList=[]
    deformed_nodes_px=[]
    #Matrices of integer pixel locations
    grid_y, grid_x = np.meshgrid(np.linspace(0, image_width-1, image_width), np.linspace(0, image_height-1, image_height), indexing='ij')

    #Interpolate nodal displacements onto pixel locations
    interp1=CloughTocher2DInterpolator(undeformed_nodes_px, displacement_px[i], fill_value=0)
    RasterPixelDisplacementMatrix = interp1(grid_y, grid_x)

    #Displace each pixel based on interpolated displacement and save greyvalue corresponding to each pixel
    for j in range(image_width):
        for k in range(image_height):
            RasterDeformedPixelList.append([float(j)+RasterPixelDisplacementMatrix[j][k][0],float(k)+RasterPixelDisplacementMatrix[j][k][1]])
            GreyvalueList.append(UndeformedImageArray[k][j])

    #Interpolate non-integer greyvalues back to pixel locations, then show final image
    interp3=CloughTocher2DInterpolator(RasterDeformedPixelList, GreyvalueList, fill_value=0)
    InterpolatedGreyvalueMatrix = (interp3(grid_y, grid_x)).T

    #save image and name according to time
    zeros='00'
    if i>=10:
        zeros='0'
    elif i>=100:
        zeros='00'
    image = Image.fromarray(InterpolatedGreyvalueMatrix.astype(np.uint8))
    image.save(folder_path+"/T"+zeros+str(i)+".tif")
    del InterpolatedGreyvalueMatrix


