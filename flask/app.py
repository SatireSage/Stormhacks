import logging

import modules.user_db as udb

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
    # vs.stitch(image_folder="/mnt/c/Stormhacks/flask/static/test-images",
    # video_name="output_video.mp4",
    # fps=1,
    # seconds_per_image=1,
    # isColor=True)

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
        else:
            logging.info(
                "Account does not exist. Please try again.", "error"
            )  # Account does not exist

    return render_template("login.html")  # Render login page


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
