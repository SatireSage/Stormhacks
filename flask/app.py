import glob
import logging
import multiprocessing
import re

import modules.user_db as udb
import modules.video_stitching as vs
import pandas
from taipy.gui import Gui

from flask import Flask
from flask import render_template
from flask import request

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum log level to DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
)


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Index method for webpage

    Parameters:
        None

    Returns:
        render_template with the base index html page

    """
    udb.initialize_db()
    try:
        udb.add_member("test", "password")  # Only add this once or check first
    except ValueError as e:
        logging.info(e)  # Handle or log this error as needed

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check user credentials
        user = udb.check_user_credentials(username, password)

        if user:
            logging.info(
                "Account exists! Login successful.", "success"
            )  # Account exists
            vs.stitch(
                image_folder="static/test-images/",
                video_name="static/videos/output_video.mp4",
                fps=1,
                seconds_per_image=1,
                isColor=True,
            )
            return render_template("showcase.html")
        else:
            logging.info(
                "Account does not exist. Please try again.", "error"
            )  # Account does not exist
            return render_template("login.html", error=True)

    return render_template("login.html")  # Render login page


# Function to run the Flask app
def run_flask():
    app.run(port=5000, use_reloader=False)


# Function to run the Taipy app
def run_taipy():
    # run_browser = False disables auto launch of browser
    taipy_page.run(port=5001, run_browser=False)


def get_photo_timestamp(photo_path):
    try:
        # Extract the date in the format YYYYMMDD
        date_match = re.search(r"_(\d{8})_(\d{6})\.jpg$", photo_path)
        if not date_match:
            return "Error: Date or time not found in filename."

        date_str = date_match.group(1)
        time_str = date_match.group(2)  # Extract the time HHMMSS

        year = date_str[0:4]  # Extract the year
        month = date_str[4:6]  # Extract the month
        day = date_str[6:8]  # Extract the day

        formatted_date = f"{year}-{month}-{day}"  # Format date as YYYY-MM-DD
        formatted_time = f"{time_str[0:2]}:{time_str[2:4]}:{time_str[4:6]}"  # Format time as HH:MM:SS

        return formatted_date, formatted_time

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

# Convert time into floating-point hours (HH.MM)
data = {
    "Date": pandas.to_datetime([date[0] for date in datetimes]),
    "Time(h)": [
        int(date[1][0:2]) + int(date[1][3:5]) / 60 + int(date[1][6:]) / 3600
        for date in datetimes
    ],  # Convert time to hours with decimals
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
