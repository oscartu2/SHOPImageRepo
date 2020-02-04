import numpy as np
import csv

class Searcher:
	def __init__(self, indexPath):
		self.indexPath = indexPath

	def chi2_distance(self, histA, histB, eps=1e-10):
		dist = 0.5 * np.sum([((a-b) ** 2)/(a+b+eps) for (a, b) in zip(histA, histB)])

		return dist

	def search(self, queryFeatures, limit = 10):
		results = {}

		with open(self.indexPath) as f:
			reader = csv.reader(f)

			for row in reader:

				# Parse out image ID and features, then compute chi-squared
				# distance between features in our index and our query features
				features = [float(x) for x in row[1:]]
				dist = self.chi2_distance(features, queryFeatures)

				# Update dictionary with key being image ID and value
				# being how "similar" the image in our index is to query
				results[row[0]] = dist

		# Sort results so smaller distances/most similar images are in front
		results = sorted([(v, k) for (k, v) in results.items()])

		# Return limited results
		return results[:limit]