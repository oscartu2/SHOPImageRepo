import ColourDescriptor

import argparse
import glob
import cv2

# Construct argument parser and parse args
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="Path to directory that contains images to be indexed")
ap.add_argument("-i", "--index", required=True, help="Path to where computed index will be stored")

args = vars(ap.parse_args())

bins = (8, 12, 3)

# Initialize ColourDescriptor
cd = ColourDescriptor.ColourDescriptor(bins)

# Open output index file for writing
with open(args["index"], "w") as output:
	# Use glob to grab image paths and loop over them
	for img_path in glob.glob(args["dataset"] + "/*.jpg"):
		# Extract image ID (unique file name) from image
		# path and load image
		image_id  = img_path[img_path.rfind("/") + 1:]
		# Could also generate UUID for image_id instead

		image = cv2.imread(img_path)

		# Describe image
		features = cd.describe(image)

		# Write features to file 
		features = [str(f) for f in features]
		output.write("%s,%s\n" % (image_id, ", ".join(features)))