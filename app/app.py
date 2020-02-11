import os
import ColourDescriptor
import Searcher

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


from skimage import io
import cv2
#import psycopg2

# Create flask instance
app = Flask(__name__)


# Main route
@app.route('/')
def index():
    return render_template('index.html')


# Search route
@app.route('/search', methods=['POST'])
def search():

	bins = (8, 12, 3)
	if request.method == 'POST':

		RESULTS_ARRAY = []

		# Get url
		image_url = request.form.get('img')

		try:
			cd = ColourDescriptor.ColourDescriptor(bins)

			# Load query image and describe it
			query = io.imread(image_url)
			query = (query * 255).astype('uint8')
			(r, g, b) = cv2.split(query)
			query = cv2.merge([b, g, r])
			features = cd.describe(query)

			# Perform search
			searcher = Searcher.Searcher(INDEX)
			results = searcher.search(features)

			# Loop over results, displaying score and image name
			for (score, result_id) in results:
				RESULTS_ARRAY.append({"image": str(result_id), "score": str(score)})

			# Return success
			return jsonify(results=(RESULTS_ARRAY[::-1][:5]))
		except:
			# Return error
			return jsonify({"sorry": "Sorry, no results! Try again"}), 500

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            print(image)

            return redirect(request.url)
            

    return render_template("index.html")



# Using CSV file with no database
INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')

# Using db
# host = "localhost"
# dbname = "postgres"
# user = "postgres"
# conn = psycopg2.connect("host=" + str(host) + " dbname=" + str(dbname) + "postgres user=" + str(user) + "postgres")
# cur = conn.cursor()
# cur.execute("""
# 	CREATE TABLE users(
# 	id integer PRIMARY KEY,
# 	featureVectors text)
# """)
# cur.execute('SELECT * FROM notes')
# one = cur.fetchone()
# all = cur.fetchall()


# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)