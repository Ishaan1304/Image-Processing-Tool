import tkinter
from tkinter import filedialog, simpledialog, messagebox
import PIL
from PIL import Image, ImageTk
import ctypes
import cv2
import numpy as np
import os

class MainWindow(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
        self.desktopWidth = width
        self.desktopHeight = height
        self.iconbitmap("icons/icon.ico")
        self.title("IMagic")
        self.geometry(f"{self.desktopWidth}x{self.desktopHeight}+0+0")
        self.state("zoomed")
        self.resizable(0, 0)

        # Menu start here
        self.menuBar = tkinter.Menu(self)
        self.config(menu=self.menuBar)
        # File menu
        self.fileMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_command(label="Open", command=self._openImage)
        self.fileMenu.add_command(label="Close")
        self.fileMenu.add_command(label="Save", command=self._save)
        self.fileMenu.add_command(label="Save as", command=self._save_as)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self._exit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        # Edit menu
        self.editMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.editMenu.add_command(label="Cut")
        self.editMenu.add_command(label="Copy")
        self.editMenu.add_command(label="Paste")
        self.menuBar.add_cascade(label="Edit", menu=self.editMenu)
        # View menu
        self.viewMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.viewMenu.add_command(label="Zoom in")
        self.viewMenu.add_command(label="Zoom out")
        self.menuBar.add_cascade(label="View", menu=self.viewMenu)

        # The view -> magnification menu
        self.magnificationMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.magnificationMenu.add_command(label="50%")
        self.magnificationMenu.add_command(label="100%")
        self.magnificationMenu.add_command(label="150%")
        self.magnificationMenu.add_command(label="200%")
        self.viewMenu.add_cascade(label="Magnification", menu=self.magnificationMenu)

        # Transform menu
        self.transformMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.transformMenu.add_command(label="Crop", command=self._cropImage)
        self.transformMenu.add_command(label="Flip Horizontal", command=self._flipHorizontal)
        self.transformMenu.add_command(label="Flip Vertical", command=self._flipVertical)
        self.menuBar.add_cascade(label="Transform", menu=self.transformMenu)

        # The Rotate -> rotate menu
        self.rotateMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.rotateMenu.add_command(label="Rotate 90\u00B0 Right", command=self._rotate90R)
        self.rotateMenu.add_command(label="Rotate 90\u00B0 Left", command=self._rotate90L)
        self.rotateMenu.add_command(label="Rotate 180\u00B0", command=self._rotate180)
        self.transformMenu.add_cascade(label="Rotate", menu=self.rotateMenu)

        # Filter menu
        self.filterMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.filterMenu.add_command(label="Mean")
        self.filterMenu.add_command(label="Median")
        self.filterMenu.add_command(label="Fourier transform")
        self.filterMenu.add_command(label="Gaussian smoothing")
        self.filterMenu.add_command(label="Unsharp")
        self.filterMenu.add_command(label="Laplacian")
        self.menuBar.add_cascade(label="Filter", menu=self.filterMenu)

        # Toolbar
        self.toolBar = tkinter.Frame(self, relief=tkinter.RAISED, bd=1, bg="antiquewhite2")
        self.toolBar.pack(side=tkinter.TOP, fill=tkinter.X)

        # Toolbar buttons
        self._load_toolbar_icons()
        self._create_toolbar_buttons()

        self.imageContainerFrame = tkinter.Frame(self, bd=1)
        self.imageContainerFrame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.imageCanvas = tkinter.Canvas(self.imageContainerFrame)
        self.imageCanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.imageFileName = None
        self.currentImage = None

        # Toolbar for imageData
        self.imageData = tkinter.Frame(self, relief=tkinter.RAISED, bd=1)
        self.imageData.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.imageDetails = tkinter.Label(self.imageData, text="Image Details: ", anchor="w")
        self.imageDetails.pack(side=tkinter.TOP, padx=2, pady=2)

    def _load_toolbar_icons(self):
        self.icons = {
            'brightness': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/brightness.gif")),
            'cut': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/cut.png")),
            'contrast': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/contrast.png")),
            'pick': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/pick.png")),
            'new': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/new.png")),
            'open': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/open.png")),
            'save': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/save.png")),
            'copy': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/copy.png")),
            'paste': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/paste.png")),
            'resize': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/resize.png")),
            'greyscale': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/greyscale.png")),
            'pan': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/pan.png")),
            'crop': PIL.ImageTk.PhotoImage(PIL.Image.open("icons/crop.png"))
        }

    def _create_toolbar_buttons(self):
        buttons = [
            ('brightness', self._brightness),
            ('cut', None),
            ('contrast', self._contrast),
            ('pick', None),
            ('new', None),
            ('open', self._openImage),
            ('save', self._save),
            ('copy', None),
            ('paste', None),
            ('resize', None),
            ('greyscale', self._greyScale),
            ('pan', None),
            ('crop', self._cropImage)
        ]
        for btn in buttons:
            button = tkinter.Button(self.toolBar, image=self.icons[btn[0]], command=btn[1])
            button.pack(side=tkinter.LEFT, padx=2, pady=2)

    def update_image_details(self):
        if self.imageFileName:
            image = Image.open(self.imageFileName)
            width, height = image.size
            _, ext = os.path.splitext(self.imageFileName)
            image_format = ext.upper()[1:]
            file_size = os.path.getsize(self.imageFileName)
            file_size_kb = file_size / 1024

            details_text = f"Image Details\n {width}x{height} pixels\n Format: {image_format}\n Size: {file_size_kb:.2f} KB\n"
            self.imageDetails.config(text=details_text)
        else:
            self.imageDetails.config(text="Image Details: No image loaded")

    def _exit(self):
        self.quit()
        self.destroy()
        exit()

    def _openImage(self):
        imgfn = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=(("png file", "*.png"), ("jpeg file", "*.jpg")))
        if imgfn:
            self.imageFileName = imgfn
            self.currentImage = ImageTk.PhotoImage(Image.open(self.imageFileName))
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")
            self.update_image_details()

    def _brightness(self):
        brightness = simpledialog.askinteger("Brightness", "Enter the value for brightness between -50 to 255", minvalue=-50, maxvalue=255)
        if brightness is not None:
            imageDataBrightness = cv2.imread(self.imageFileName)
            if imageDataBrightness is not None:
                imageDataBrightness = cv2.convertScaleAbs(imageDataBrightness, alpha=1, beta=brightness)
                imageDataRGB_forBrightness = cv2.cvtColor(imageDataBrightness, cv2.COLOR_BGR2RGB)
                pillowBrightness = Image.fromarray(imageDataRGB_forBrightness)
                self.currentImage = ImageTk.PhotoImage(pillowBrightness)
                self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _contrast(self):
        contrast = simpledialog.askinteger("Contrast", "Enter the value for contrast between -125 to 255", minvalue=-125, maxvalue=255)
        if contrast is not None:
            imageDataContrast = cv2.imread(self.imageFileName)
            if imageDataContrast is not None:
                f = (259 * (contrast + 255)) / (255 * (259 - contrast))
                imageDataContrast = cv2.convertScaleAbs(imageDataContrast, alpha=f, beta=0)
                imageDataRGB_forContrast = cv2.cvtColor(imageDataContrast, cv2.COLOR_BGR2RGB)
                pillowContrast = Image.fromarray(imageDataRGB_forContrast)
                self.currentImage = ImageTk.PhotoImage(pillowContrast)
                self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _greyScale(self):
        imageData = cv2.imread(self.imageFileName)
        if imageData is not None:
            greyScaleImage = cv2.cvtColor(imageData, cv2.COLOR_BGR2GRAY)
            pillowGreyScale = Image.fromarray(greyScaleImage)
            self.currentImage = ImageTk.PhotoImage(pillowGreyScale)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _rotate90R(self):
        if self.currentImage:
            image = Image.open(self.imageFileName)
            rotated_image = image.rotate(-90, expand=True)
            self.currentImage = ImageTk.PhotoImage(rotated_image)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _rotate90L(self):
        if self.currentImage:
            image = Image.open(self.imageFileName)
            rotated_image = image.rotate(90, expand=True)
            self.currentImage = ImageTk.PhotoImage(rotated_image)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _rotate180(self):
        if self.currentImage:
            image = Image.open(self.imageFileName)
            rotated_image = image.rotate(180, expand=True)
            self.currentImage = ImageTk.PhotoImage(rotated_image)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _flipHorizontal(self):
        if self.currentImage:
            image = Image.open(self.imageFileName)
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            self.currentImage = ImageTk.PhotoImage(flipped_image)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _flipVertical(self):
        if self.currentImage:
            image = Image.open(self.imageFileName)
            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            self.currentImage = ImageTk.PhotoImage(flipped_image)
            self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _cropImage(self):
        if self.currentImage:
            image = Image.open(self.imageFileName)
            left = simpledialog.askinteger("Crop", "Enter the left coordinate")
            top = simpledialog.askinteger("Crop", "Enter the top coordinate")
            right = simpledialog.askinteger("Crop", "Enter the right coordinate")
            bottom = simpledialog.askinteger("Crop", "Enter the bottom coordinate")
            if left is not None and top is not None and right is not None and bottom is not None:
                cropped_image = image.crop((left, top, right, bottom))
                self.currentImage = ImageTk.PhotoImage(cropped_image)
                self.imageCanvas.create_image(0, 0, image=self.currentImage, anchor="nw")

    def _save(self):
        if self.imageFileName:
            image = Image.open(self.imageFileName)
            image.save(self.imageFileName)
            messagebox.showinfo("Save Image", "Image saved successfully")

    def _save_as(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if save_path:
            image = Image.open(self.imageFileName)
            image.save(save_path)
            self.imageFileName = save_path
            messagebox.showinfo("Save Image", "Image saved successfully")

if __name__ == "__main__":
    mainWindow = MainWindow()
    mainWindow.mainloop()
