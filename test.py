import subprocess
import time

from flask import Flask
from flask import render_template

# Create a Flask app
app = Flask(__name__)


# Start the Taipy app in a separate subprocess
def start_taipy():
    # Use subprocess to run the Taipy app in the background
    subprocess.Popen(["python3", "taipy_app.py"])


# Flask route to render the HTML with embedded Taipy iframe
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # Start Taipy first
    start_taipy()
    # Wait a bit to ensure the Taipy app is running
    time.sleep(2)  # Adjust the time as needed
    # Start Flask on port 5000
    app.run(port=5000, debug=True, use_reloader=False)
