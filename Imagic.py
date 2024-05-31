import tkinter
from tkinter import filedialog, simpledialog, messagebox
import PIL
import ctypes
from PIL import Image, ImageTk
from PIL import Image
import cv2
import numpy
import os

class MainWindow(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        width,height=ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1)
        self.desktopWidth=width
        self.desktopHeight=height
        self.iconbitmap("icons/icon.ico")
        self.title("IMagic")
        self.geometry(str(self.desktopWidth)+"x"+str(self.desktopHeight)+"+0+0")
        self.state("zoomed")
        self.resizable(0,0)

        #Menu start here
        self.menuBar=tkinter.Menu(self)
        self.config(menu=self.menuBar)
        #File menu
        self.fileMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_command(label="Open",command=self._openImage)
        self.fileMenu.add_command(label="Close")
        self.fileMenu.add_command(label="Save",command=self._save)
        self.fileMenu.add_command(label="Save as")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit",command=self._exit)
        self.menuBar.add_cascade(label="File",menu=self.fileMenu)
        #Edit menu
        self.editMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.editMenu.add_command(label="Cut")
        self.editMenu.add_command(label="Copy")
        self.editMenu.add_command(label="Paste")
        self.menuBar.add_cascade(label="Edit",menu=self.editMenu)
        # view menu
        self.viewMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.viewMenu.add_command(label="Zoom in")
        self.viewMenu.add_command(label="Zoom out")
        self.menuBar.add_cascade(label="View",menu=self.viewMenu)

        #the view -> magnification menu
        self.magnificationMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.magnificationMenu.add_command(label="50%")
        self.magnificationMenu.add_command(label="100%")
        self.magnificationMenu.add_command(label="150%")
        self.magnificationMenu.add_command(label="200%")
        self.viewMenu.add_cascade(label="Magnification",menu=self.magnificationMenu)
        
        #Transform menu
        self.transformMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.transformMenu.add_command(label="Crop",command=self._cropImage)
        self.transformMenu.add_command(label="Flip Horizontal",command=self._flipHorizontal)
        self.transformMenu.add_command(label="Flip Vertical",command=self._flipVertical)
        self.menuBar.add_cascade(label="Transform",menu=self.transformMenu)
        
        #the Rotate -> rotate menu
        self.rotateMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.rotateMenu.add_command(label="Rotate 90\u00B0 Right",command=self._rotate90R)
        self.rotateMenu.add_command(label="Rotate 90\u00B0 Left",command=self._rotate90L)
        self.rotateMenu.add_command(label="Rotate 180\u00B0",command=self._rotate180)
        self.transformMenu.add_cascade(label="Rotate",menu=self.rotateMenu)

        # filter menu
        self.filtermMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.filtermMenu.add_command(label="Mean")
        self.filtermMenu.add_command(label="Median")
        self.filtermMenu.add_command(label="Fourier transform")
        self.filtermMenu.add_command(label="Gaussian smoothing")
        self.filtermMenu.add_command(label="Unsharp")
        self.filtermMenu.add_command(label="Laplacian")
        self.menuBar.add_cascade(label="Filter",menu=self.filtermMenu)

        #Tool bar
        self.toolBar=tkinter.Frame(self,relief=tkinter.RAISED,bd=1,bg="antiquewhite2")
        self.toolBar.pack(side=tkinter.TOP,fill=tkinter.X)
      
        #ToolBar button

        self.imageBrightness=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/brightness.gif"))
        self.toolBarBrightnessButton=tkinter.Button(self.toolBar,image=self.imageBrightness,command=self._brightness)
        self.toolBarBrightnessButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageCut=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/cut.png"))
        self.toolBarCutButton=tkinter.Button(self.toolBar,image=self.imageCut)
        self.toolBarCutButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageContrast=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/contrast.png"))
        self.toolBarContrastButton=tkinter.Button(self.toolBar,image=self.imageContrast,command=self._contrast)
        self.toolBarContrastButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        

        self.imagePick=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/pick.png"))
        self.toolBarPickButton=tkinter.Button(self.toolBar,image=self.imagePick)
        self.toolBarPickButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageNew=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/new.png"))
        self.toolBarNewButton=tkinter.Button(self.toolBar,image=self.imageNew)
        self.toolBarNewButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageOpen=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/open.png"))
        self.toolBarOpenButton=tkinter.Button(self.toolBar,image=self.imageOpen,command=self._openImage)
        self.toolBarOpenButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageSave=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/save.png"))
        self.toolBarSaveButton=tkinter.Button(self.toolBar,image=self.imageSave,command=self._save)
        self.toolBarSaveButton.pack(side=tkinter.LEFT,padx=2,pady=2)
        

        self.imageCopy=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/copy.png"))
        self.toolBarCopyButton=tkinter.Button(self.toolBar,image=self.imageCopy)
        self.toolBarCopyButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imagePaste=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/paste.png"))
        self.toolBarPasteButton=tkinter.Button(self.toolBar,image=self.imagePaste)
        self.toolBarPasteButton.pack(side=tkinter.LEFT,padx=2,pady=2)
   

        self.imageResize=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/resize.png"))
        self.toolBarResizeButton=tkinter.Button(self.toolBar,image=self.imageResize)
        self.toolBarResizeButton.pack(side=tkinter.LEFT,padx=2,pady=2)
 
        self.imageGreyscale=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/greyscale.png"))
        self.toolBarGreyscaleButton=tkinter.Button(self.toolBar,image=self.imageGreyscale,command=self._greyScale)
        self.toolBarGreyscaleButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imagePan=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/pan.png"))
        self.toolBarPanButton=tkinter.Button(self.toolBar,image=self.imagePan)
        self.toolBarPanButton.pack(side=tkinter.LEFT,padx=2,pady=2)
       

        self.imageCrop=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/crop.png"))
        self.toolBarCropButton=tkinter.Button(self.toolBar,image=self.imageCrop,command=self._cropImage)
        self.toolBarCropButton.pack(side=tkinter.LEFT,padx=2,pady=2)
    
        self.imageContainerFrame=tkinter.Frame(self,bd=1)
        self.imageContainerFrame.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)
        self.imageCanvas=tkinter.Canvas(self.imageContainerFrame)
        self.imageCanvas.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)
        self.imageFileName=None
        self.currentImage=None

        #ToolBar for imagData
        self.imageData=tkinter.Frame(self,relief=tkinter.RAISED,bd=1)
        self.imageData.pack(side=tkinter.RIGHT,fill=tkinter.Y)

        self.imageDetails = tkinter.Label(self.imageData, text="Image Details: ", anchor="w")
        self.imageDetails.pack(side=tkinter.TOP, padx=2, pady=2)

    def update_image_details(self):
        if self.imageFileName:
            # Get image dimensions
            image = Image.open(self.imageFileName)
            width, height = image.size
            # Get image format
            _, ext = os.path.splitext(self.imageFileName)
            image_format = ext.upper()[1:]  # Remove dot and convert to uppercase
            # Image size
            file_size = os.path.getsize(self.imageFileName)
            file_size_kb = file_size / 1024  # Convert bytes to kilobytes

            # Update label text
            details_text = f"Image Details\n {width}x{height} pixels\n Format: {image_format}\n Size: {file_size_kb:.2f} KB\n"
            self.imageDetails.config(text=details_text)
        else:
            self.imageDetails.config(text="Image Details: No image loaded")
        
        
        
   
         

        
    
    def _exit(self):
        self.quit()
        self.destroy()
        exit()


         
    def _openImage(self):
        imgfn=tkinter.filedialog.askopenfilename(initialdir="/",title="Select Image File",filetypes=(("png file","*.png"),("jpeg file","*.jpg")))
        if imgfn is None:
            messagebox.showwarning("Warning","Please select image !")
        else:   
            self.imageFileName=imgfn
            self.currentImage=PIL.ImageTk.PhotoImage(PIL.Image.open(self.imageFileName))
            self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")
            self.update_image_details()



    def _brightness(self):
        brightness = None  # Assigning a default value to brightness
        brightnessImage = simpledialog.askstring(title="Brightness", prompt="Enter the value for brightness between -50 to 255")
        if brightnessImage is not None:
            try:
                brightness = int(brightnessImage)
                if -50 <= brightness <= 255:  
                    imageDataBrightness = cv2.imread(self.imageFileName)
                    if imageDataBrightness is not None:
                        for r in range(imageDataBrightness.shape[0]):
                            for c in range(imageDataBrightness.shape[1]):
                               rgb = imageDataBrightness[r][c]
                               red = rgb[2]
                               green = rgb[1]  
                               blue = rgb[0] 
                               red += brightness
                               green += brightness
                               blue += brightness
                               if red > 255: red = 255
                               if red < 0: red = 0
                               if green > 255: green = 255
                               if green < 0: green = 0
                               if blue > 255: blue = 255
                               if blue < 0: blue = 0
                               imageDataBrightness[r][c] = (blue, green, red) 
                        imageDataRGB_forBrightness = cv2.cvtColor(imageDataBrightness, cv2.COLOR_BGR2RGB)
                        pillowBrightness = Image.fromarray(imageDataRGB_forBrightness)
                        self.currentImage = ImageTk.PhotoImage(pillowBrightness)
                        self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")
                    else:
                        messagebox.showwarning("Warning","Failed to load image")
                else:
                    messagebox.showwarning("Warning", "Value of brightness must be between -50 to 255")
            except ValueError:
                if brightnessImage.strip():
                    messagebox.showwarning("Warning","Only integers are allowed")
                else:
                    messagebox.showwarning("Warning", "Please provide an integer value for brightness")
        
        


        
        
    def _contrast(self):
        contrastImage=simpledialog.askstring(title="Contrast",prompt="Enter the value for contrast between -125 to 255")
        if contrastImage is not None:
            try:
                contrast=int(contrastImage)
                if -125 <= contrast <= 255:
                    imageDataContrast=cv2.imread(self.imageFileName)
                    if imageDataContrast is not None:
                        f=(259*(contrast+255))/(255*(259-contrast))
                        for r in range(imageDataContrast.shape[0]):
                            for c in range(imageDataContrast.shape[1]):
                                rgb=imageDataContrast[r][c]
                                red=rgb[2]
                                green=rgb[1]
                                blue=rgb[0]
                                newRed=(f*(blue-128))+128 
                                newGreen=(f*(green-128))+128
                                newBlue=(f*(blue-128))+128
                                if newRed>255: newRed=255
                                if newRed<0: newRed=0
                                if newGreen>255: newGreen=255
                                if newGreen<0: newGreen=0
                                if newBlue>255: newBlue=255
                                if newBlue<0: newBlue=0
                                imageDataContrast[r][c]=(newRed,newGreen,newBlue)
                        imageDataRGB_forContrast = cv2.cvtColor(imageDataContrast, cv2.COLOR_BGR2RGB)
                        pillowContrast = Image.fromarray(imageDataRGB_forContrast)
                        self.currentImage = ImageTk.PhotoImage(pillowContrast)
                        self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")
                    else:
                        messagebox.showwarning("Warning","Failed to load image") 
                else:
                    messagebox.showwarning("Warning", "Value of contrast must be between -125 to 255")
            except ValueError:
                if contrastImage.strip():
                    messagebox.showwarning("Warning","Only integers are allowed")
                else:
                    messagebox.showwarning("Warning", "Please provide an integer value for contrast")
        



    def _greyScale(self):
        greyScaleImage=simpledialog.askstring(title="Grey",prompt="Enter the value for GreyScale between -20 to 100")
        if greyScaleImage is not None:
            try:
                greyScale=int(greyScaleImage)
                if -20 <= greyScale <= 100:
                    imageDataGreyScale=cv2.imread(self.imageFileName)
                    if imageDataGreyScale is not None:   
                        for r in range(imageDataGreyScale.shape[0]):
                            for c in range(imageDataGreyScale.shape[1]):
                                rgb=imageDataGreyScale[r][c]
                                red=rgb[2]
                                green=rgb[1]
                                blue=rgb[0]
                                red=(int(rgb[2]*0.3))
                                green=(int(rgb[1]*0.59))
                                blue=(int(rgb[0]*0.11))
                                total=red+green+blue
                                imageDataGreyScale[r][c]=(total,total,total)
                        imageDataRGB_forGreyScale = cv2.cvtColor(imageDataGreyScale, cv2.COLOR_BGR2RGB)
                        pillowGreyScale = Image.fromarray(imageDataRGB_forGreyScale)
                        self.currentImage = ImageTk.PhotoImage(pillowGreyScale)
                        self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")
                    else:
                        messagebox.showwarning("Warning","Failed to load image")
                else:
                    messagebox.showwarning("Warning", "Value of contrast must be between -20 to 100")   

            except ValueError:    
                if greyScaleImage.strip():
                    messagebox.showwarning("Warning","Only integers are allowed")
                else:
                    messagebox.showwarning("Warning", "Please provide an integer value for brightness")

   
    def _cropImage(self):
        cropImage = simpledialog.askstring(title="Crop", prompt="Enter the value of Height and Width to crop")
        if cropImage is not None:
            try:
                cropWidth, cropHeight = map(int, cropImage.split(','))
                cropImageData = cv2.imread(self.imageFileName)
                if cropImageData is not None:
                    cropFrom = (0, 0)
                    cropSize = (cropWidth, cropHeight)
                    c1, r1 = cropFrom
                    c2, r2 = c1 + cropSize[0] - 1, r1 + cropSize[1] - 1
                    if r2 >= cropImageData.shape[0]:
                        r2 = cropImageData.shape[0] - 1
                    if c2 >= cropImageData.shape[1]:
                        c2 = cropImageData.shape[1] - 1
                    newImage = numpy.zeros((cropSize[1], cropSize[0], 3))
                    rr = 0
                    r = r1
                    while r <= r2:
                        cc = 0
                        c = c1
                        while c <= c2:
                            newImage[rr][cc] = cropImageData[r][c]
                            cc += 1
                            c += 1
                        rr += 1
                        r += 1
                    newImage = cv2.imwrite("newImage")
                    messagebox.showinfo("Information","Image save succesfully")
                else:
                    messagebox.showwarning("Warning", "Failed to load the image.")
            except ValueError:
                if cropImage.strip():
                    messagebox.showwarning("Warning","Only integers are allowed")
                else:
                    messagebox.showwarning("Warning", "Please provide an integer value for croping image")

    def _rotate180(self):
        imageDataRotate180=cv2.imread(self.imageFileName)
        if imageDataRotate180 is not None:
            imageRotate180 = cv2.rotate(imageDataRotate180, cv2.ROTATE_180)
            imageDataRGB_forRotate180 = cv2.cvtColor(imageRotate180, cv2.COLOR_BGR2RGB)
            pillowRotate180 = Image.fromarray(imageDataRGB_forRotate180)
            self.currentImage = ImageTk.PhotoImage(pillowRotate180)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")
        else:
            messagebox.showwarning("Warning","Image is not found !")

    def _rotate90R(self):
        imageDataRotate90R=cv2.imread(self.imageFileName)
        if imageDataRotate90R is not None:
            imageRotate90R = cv2.rotate(imageDataRotate90R, cv2.ROTATE_90_CLOCKWISE)
            imageDataRGB_forRotate90R = cv2.cvtColor(imageRotate90R, cv2.COLOR_BGR2RGB)
            pillowRotate90R = Image.fromarray(imageDataRGB_forRotate90R)
            self.currentImage = ImageTk.PhotoImage(pillowRotate90R)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")
        else:
            messagebox.showwarning("Warning","Image is not found !")

    def _rotate90L(self):
        imageDataRotate90L=cv2.imread(self.imageFileName)
        if imageDataRotate90L is not None:
            imageRotate90L = cv2.rotate(imageDataRotate90L, cv2.ROTATE_90_COUNTERCLOCKWISE)
            imageDataRGB_forRotate90L = cv2.cvtColor(imageRotate90L, cv2.COLOR_BGR2RGB)
            pillowRotate90L = Image.fromarray(imageDataRGB_forRotate90L)
            self.currentImage = ImageTk.PhotoImage(pillowRotate90L)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")        
        else:
            messagebox.showwarning("Warning","Image is not found !")

    def _flipHorizontal(self):
        imageDataFlipHorizontal=cv2.imread(self.imageFileName)
        if imageDataFlipHorizontal is not None:
            imageFlipHorizontal = cv2.flip(imageDataFlipHorizontal,1)
            imageDataRGB_forFlipH = cv2.cvtColor(imageFlipHorizontal, cv2.COLOR_BGR2RGB)
            pillowFlipH = Image.fromarray(imageDataRGB_forFlipH)
            self.currentImage = ImageTk.PhotoImage(pillowFlipH)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")
        else:
            messagebox.showwarning("Warning","Image is not found !")

    def _flipVertical(self):
        imageDataFlipVertical=cv2.imread(self.imageFileName)
        if imageDataFlipVertical is not None:
            imageFlipVertical = cv2.flip(imageDataFlipVertical,0)
            imageDataRGB_forFlipV = cv2.cvtColor(imageFlipVertical, cv2.COLOR_BGR2RGB)
            pillowFlipV = Image.fromarray(imageDataRGB_forFlipV)
            self.currentImage = ImageTk.PhotoImage(pillowFlipV)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")
        else:
            messagebox.showwarning("Warning","Image is not found !")

    def _save(self):
        if self.currentImage is not None:
            save_path = tkinter.filedialog.asksaveasfilename(initialdir="/", title="Save Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")))
            if save_path:  # Check if user selected a file
                pil_image = Image.open(self.imageFileName)
                pil_image.save(save_path)
                messagebox.showinfo("Information", "Image saved successfully!")
        else:
            messagebox.showwarning("Warning", "Image is not found!")

    


                     
          
mainwindow=MainWindow()
mainwindow.mainloop()

