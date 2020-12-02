from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import numpy as np
from matplotlib import pyplot as plt 


# global variables
window = None
originalImage = None
image = False
imageL = None


def main():
	# create window
	window = Tk()
	window.title("IP Project")
	window.resizable(False, False)

	# seprate function to deal with window elements and design
	createWidgets()
	
	# start window
	window.mainloop()

def createWidgets():
	"""A function that create widgets and attach them to the main golabal window object.
	It deals with design and attaching functionality to each button.
	It doesn't require any parameters and doesn't return any values.
	But it does require a global window variable declared and initialized."""


	# Basic Operations Section
	basicL = Label(window, text="Basic Operations", width=20, height=2, font="None 10 bold")
	basicL.grid(row=0, column=0, columnspan=2, rowspan=2, padx=20, pady=20)

	uploadB = Button(window, text="Upload Image", command=upload, width=20, height=2, font="None 10 bold")
	uploadB.grid(row=2, column=0, columnspan=2)

	greyB = Button(window, text="RGB to Gray", command=toGray, width=20, height=2, font="None 10 bold")
	greyB.grid(row=3, column=0, columnspan=2)

	binaryB = Button(window, text="Convert to Binary Image", command=toBinary, width=20, height=2, font="None 10 bold")
	binaryB.grid(row=4, column=0, columnspan=2)

	resetB = Button(window, text="RESET", command=reset, width=20, height=2, font="None 10 bold")
	resetB.grid(row=5, column=0, columnspan=2)
	

	# Image Section
	global imageL

	# create gray background image as a start
	img = np.ones([512,512,1],dtype=np.uint8) * 100
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = Image.fromarray(img)
	img = ImageTk.PhotoImage(img)

	imageL = Label(window, image=img, borderwidth=2, relief="solid", bg="#CCCCCC")
	imageL.grid(row=0, column=2, columnspan=8, rowspan=6, pady=20, padx=20)


	# Advanced Operations Section
	advancedL = Label(window, text="Advanced Operations", width=20, height=2, font="None 10 bold")
	advancedL.grid(row=6, column=0, columnspan=2, padx=20, pady=20)
	
	histogramB = Button(window, text="Histogram", command=histogram, width=20, height=2, font="None 10 bold")
	histogramB.grid(row=6, column=2, padx=10)

	complementB = Button(window, text="Complement Image", command=complement, width=20, height=2, font="None 10 bold")
	complementB.grid(row=6, column=3, padx=10)

	edgeB = Button(window, text="Edge Detection", command=detectEdges, width=20, height=2, font="None 10 bold")
	edgeB.grid(row=6, column=4, padx=10)

	rotateB = Button(window, text="Rotate Clockwise", command=rotate, width=20, height=2, font="None 10 bold")
	rotateB.grid(row=7, column=2, padx=10)

	antirotateB = Button(window, text="Rotate Anti-Clockwise", command=antiRotate, width=20, height=2, font="None 10 bold")
	antirotateB.grid(row=7, column=3, padx=10, pady=20)



# Operations

def update():
	"""A function that updates the window image to match the last modifications"""
	global image
	global imageL

	# convert image from cv2 form to TK form
	img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	img = Image.fromarray(img)
	img = ImageTk.PhotoImage(img)

	# update the image label in the window
	imageL.configure(image=img)
	imageL.image = img


def upload():
	"""A function that deals with uploading an image from local storage to the window"""
	global image
	global originalImage 
	
	# get path
	path = filedialog.askopenfilename()
	if not path:
		return

	# read the image into cv form
	image = cv2.imread(path)
	image = cv2.resize(image, (512, 512))

	# create a copy from the original image 
	originalImage = image.copy()

	update()


def toGray():
	"""A function that converts RGB image to gray on window"""
	global image

	# make sure that an image is uploaded
	if type(image) == type(False):
		return

	# helper function to convert image to gray
	convertToGrey()

	update()


def toBinary():
	"""A function that converts RGB or gray images to binary on window using 127 as threshold"""
	global image

	# make sure that an image is uploaded
	if type(image) == type(False):
		return

	# convert to gray first
	convertToGrey()

	# converting to binary
	ret, image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)

	update()


def reset():
	"""A function that resets image on screen to its original form"""
	global image
	global originalImage 

	# make sure that an image is uploaded
	if type(image) == type(False):
		return

	# restore from original image
	image = originalImage.copy()

	update()


def histogram():
	"""A function that outputs a histogram plot on screen from the current image.
	It works with both RGB and gray images."""
	global image

	# make sure that an image is uploaded
	if type(image) == type(False):
		return

	# in case image is RGB
	if len(image.shape) == 3:
		color = ('b','g','r')
		for i, col in enumerate(color):
			# calculate and plot histogram for each channel
			hist = cv2.calcHist([image],[i],None,[256],[0,256])
			plt.plot(hist,color = col)

	# in case inage is grayscale
	else:
		# calculate and plot histogram
		hist = cv2.calcHist([image],[0],None,[256],[0,256]) 
		plt.plot(hist)

	# show the histogram in a new window
	plt.xlim([0,256]) 
	plt.show() 


def complement():
	"""A function that converts image to its complement no matter what form it's in"""
	global image

	# make sure that an image is uploaded
	if type(image) == type(False):
		return

	# make conversion
	image = 255 - image

	update()


def detectEdges():
	"""A function that detect edges of an image using laplacian method"""
	global image

	# make sure that an image is uploaded
	if type(image) == type(False):
		return
	
	# convert image to grayscale first
	convertToGrey()

	# use median blur to reduce noise for better results
	image = cv2.medianBlur(image, 3)
	
	# detect edges using laplacian 
	image = cv2.Laplacian(image, ksize=3, ddepth=cv2.CV_16S)
	image = cv2.convertScaleAbs(image)

	update()


def rotate():
	"""A function that rotates the image 90 degrees clockwise on screen"""
	global image

	# make sure that an image is uploaded
	if type(image) == type(False):
		return
	
	# rotate 
	image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
	update()
	

def antiRotate():
	"""A function that rotates the image 90 degrees counter clockwise on screen"""
	global image

	# make sure that an image is uploaded
	if type(image) == type(False):
		return
	
	# rotate
	image = cv2.rotate(image, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
	update()


# Helper Functions

def convertToGrey():
	"""a function that converts image to grayscale if image is RGB and do not deal with the window"""
	global image
	
	# make sure it's RGB form
	if len(image.shape) == 3:
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# run program at start
if __name__== "__main__":
	main()