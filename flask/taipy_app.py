import glob
import multiprocessing
import re

import pandas
from PIL import Image
from PIL.ExifTags import TAGS
from taipy.gui import Gui

from flask import Flask
from flask import render_template

# Create the Flask app
app = Flask(__name__)


# Define the Flask route for the homepage
@app.route("/")
def index():
    return render_template("progresspics.html")


# Function to run the Flask app
def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)


# Function to run the Taipy app
def run_taipy():
    # run_browser = False disables auto launch of browser
    taipy_page.run(port=5001, run_browser=False)


def get_photo_timestamp(photo_path):
    try:
        # Open the image file
        img = Image.open(photo_path)

        # Extract EXIF data
        exif_data = img._getexif()

        # Dictionary to hold the extracted EXIF data
        exif_info = {}

        # Loop through the EXIF tags
        if exif_data:
            for tag, value in exif_data.items():
                decoded_tag = TAGS.get(tag, tag)
                exif_info[decoded_tag] = value

            # Return the DateTimeOriginal (when the photo was taken)
            timestamp = exif_info.get("DateTimeOriginal", "No Timestamp Found")
            img.close()
            return re.findall(r"\d+:\d+:\d+", timestamp)
        else:
            img.close()
            return None

    except Exception as e:
        return f"Error: {e}"


# Glob the directory and get all photos then parse timestamp data
photos = glob.glob("static/images/*")
datetimes = []
for photo in photos:
    metadata = get_photo_timestamp(photo)
    if metadata is not None:
        datetimes.append(metadata)
# Data to display in the chart
# Convert the pairs into a single datetime object
datetimes.sort()
data = {
    "Date": pandas.to_datetime(
        [date[0].replace(":", ";") for date in datetimes]
    ),  # Convert dates to datetime
    "Time(h)": [
        int(date[1][0] + date[1][1]) for date in datetimes
    ],  # Convert times to time objects
}

page = """
<|{data}|chart|mode=lines|x=Date|y=Time(h)|>
"""

# Taipy GUI setup
taipy_page = Gui(page)

if __name__ == "__main__":
    # Create processes for Flask and Taipy
    flask_process = multiprocessing.Process(target=run_flask)
    taipy_process = multiprocessing.Process(target=run_taipy)

    # Start both processes
    flask_process.start()
    taipy_process.start()

    # Wait for both processes to finish
    flask_process.join()
    taipy_process.join()