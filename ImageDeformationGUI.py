from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
import subprocess
from PIL import ImageTk, Image
import os
import GenerateDeformedImages

#Run odb_structure.py with given odb file and name output .csv file
def RunABAQUSScript():
    csvname = simpledialog.askstring("Name output .csv file", "Name output .csv file")
    odb = filedialog.askopenfilename(initialdir = "/EvanWey/ImageDeformationPackage", title = "Select a File", filetypes = (("Text files","*.txt *.odb"),("all files","*.*")))
    subprocess.run(["start", "/wait", "cmd", "/K", "abaqus python C:\EvanWey\ImageDeformationPackage\odb_structure.py "+odb+" "+csvname], shell=True)

def OpenImage():
    x = filedialog.askopenfilename(title ='Select Image...', filetypes = (("Image files", "*.png *.jpg *.jpeg *.tif"),("all files","*.*")))
    img = Image.open(x)
    imgwidth,imgheight=img.size
    img = img.resize((int(imgwidth/4),int(imgheight/4)), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel = Label(frm, image = img)
    panel.image = img
    panel.grid(row = 2, column=0, columnspan=3,pady=20)

#Displays a preview of an image with imposed nodes    
def ImposeMesh():
    csv = filedialog.askopenfilename(initialdir = "/EvanWey/ImageDeformationPackage", title = "Select a .csv file", filetypes = (("CSV files", "*.csv"),("all files","*.*")))
    scale=simpledialog.askstring("Scale", "mm/pixel scale: ")
    undeformed_nodes,displacements,timeIncrements=GenerateDeformedImages.LoadCSV(csv,scale)
    image = filedialog.askopenfilename(initialdir = "/EvanWey/ImageDeformationPackage", title = "Select an image file", filetypes = (("Image files", "*.png *.jpg *.jpeg *.tif"),("all files","*.*")))
    imposed_image=GenerateDeformedImages.ImposeNodes(image,undeformed_nodes)
    imgwidth,imgheight=imposed_image.size
    if imgwidth>1000:
         imposed_image.resize((int(imgwidth/4),int(imgheight/4)), Image.LANCZOS)
    imposed_image = ImageTk.PhotoImage(imposed_image)
    panel = Label(frm, image = imposed_image)
    panel.image = imposed_image
    panel.grid(row = 2, column=0, columnspan=3,pady=20)

def DeformImages():
    csv = filedialog.askopenfilename(initialdir = "/EvanWey/ImageDeformationPackage", title = "Select a .csv file", filetypes = (("CSV files", "*.csv"),("all files","*.*")))
    scale=simpledialog.askstring("Scale", "mm/pixel scale: ")
    undeformed_nodes,displacements,timeIncrements=GenerateDeformedImages.LoadCSV(csv,scale)
    image = filedialog.askopenfilename(initialdir = "/EvanWey/ImageDeformationPackage", title = "Select an image file", filetypes = (("Image files", "*.png *.jpg *.jpeg *.tif"),("all files","*.*")))
    foldername = simpledialog.askstring("Name output folder", "Name output folder")
    GenerateDeformedImages.DeformImages(image,foldername,timeIncrements,undeformed_nodes,displacements)
    
#Create window
def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

window = create_widget(None, Tk)
window.title("Image Deformation Package")
window.resizable(width = True, height = True)
frm = ttk.Frame(window, padding=20)
frm.grid()

#Extracting displacements from ABAQUS using odb_structure.py
ttk.Label(frm, text="Extract displacements from ABAQUS").grid(column=0, row=0, padx=20,pady=20)
ttk.Label(frm, text=".odb file:").grid(column=1, row=0, padx=10,pady=20)
button_explore = Button(frm, text = "Browse Files", command = RunABAQUSScript).grid(column=2, row=0, padx=10,pady=20)

#Impose FE nodes onto image
btn = Button(frm, text ='Open Image', command = OpenImage).grid(column=0, row = 1, columnspan=1,pady=20)
ttk.Label(frm, text="Image Preview:").grid(column=1, row=1, columnspan=1,pady=20)
btn = Button(frm, text ='Impose Mesh', command = ImposeMesh).grid(column=2, row = 1, columnspan=1,pady=20)

btn = Button(frm, text ='Generate Deformed Images', command = DeformImages).grid(column=0, row = 3, columnspan=3,pady=20)
ttk.Label(frm, text="Warning: may take a long time for higher resolution images", foreground='red').grid(column=0, row=4, columnspan=3)




window.mainloop()