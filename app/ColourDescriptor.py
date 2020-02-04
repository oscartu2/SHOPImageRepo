import numpy as np
import cv2
import imutils

class ColourDescriptor:
	def __init__(self, bins):
		# Store number of bins for 3D Histogram
		self.bins = bins

	def histogram(self, image, mask):
		# Extract a 3D color histogram from masked region of image,
		# using specified number of bins per channel
		hist = cv2.calcHist([image], [0,1,2], mask, self.bins, [0, 180, 0, 256, 0, 256])

		hist = cv2.normalize(hist, hist).flatten()

		return hist

	def describe(self, image):
		# Convert image to HSV color space and
		# initialize features used to quantify the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []

		# Get image dimensions and compute center
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w*0.5), int(h*0.5))

		# Divide image into 4 rectangular sections, top left,
		# bottom left, top right, bottom right
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

		# Make center eliptical mask
		(axesX, axesY) = (int(w*0.75)//2, int(h*0.75)//2)
		ellipMask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

		# Loop over segments
		for (startX, endX, startY, endY) in segments:

			# Make mask for each corner of image, and subtract elliptical
			# center from it
			cornerMask = np.zeros(image.shape[:2], dtype="uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)

			# Extract a color histogram from the image,
			# then update feature vector
			features.extend(self.histogram(image, cornerMask))

		# Extract a color histogram from the elliptical region,
		# then update feature vector
		features.extend(self.histogram(image, ellipMask))
		return features










