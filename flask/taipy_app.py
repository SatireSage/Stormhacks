# from taipy import Gui
#
# list_to_display = [100/x for x in range(1, 100)]
# image_path = "/Users/sahajsingh/Downloads/test.png"  # Use the actual path to your local image
#
# # GUI definition with local image
# page = f"""
# <|{{list_to_display}}|chart|>
#
# <|{{image_path}}|image|>
# """
#
# Gui(page).run()

###################################################

# from taipy import Gui
#
# list_to_display = [100/x for x in range(1, 100)]
# video_path = "/Users/sahajsingh/Downloads/colton.mp4"  # Replace this with your actual local video path
#
# # GUI definition with local video
# page = f"""
# <|{{list_to_display}}|chart|>
#
# <video width="400" height="300" controls>
#   <source src="{video_path}" type="video/mp4" />
#   Your browser does not support the video tag.
# </video>
# """
#
# Gui(page).run()

###################################################

# from flask import Flask
# from taipy.gui import Gui
# import threading
#
# # Create the Flask app
# app = Flask(__name__)
#
# # Data to display in the chart
# list_to_display = [100/x for x in range(1, 100)]
#
# page = f"""
# <|{{list_to_display}}|chart|>
# """
#
# # Taipy GUI setup
# taipy_page = Gui(page)
#
# # Define the Flask route for the homepage
# @app.route('/')
# def index():
#     return """
#     <h1>Welcome to the Flask Homepage!</h1>
#     <p><a href="http://localhost:5001/">Go to Taipy Page</a></p>
#     """
#
# # Function to run the Flask app
# def run_flask():
#     app.run(debug=True, port=5000, use_reloader=False)
#
# # Function to run the Taipy app
# def run_taipy():
#     taipy_page.run(port=5001)
#
# if __name__ == "__main__":
#     # Run Flask and Taipy on separate threads
#     flask_thread = threading.Thread(target=run_flask)
#     taipy_thread = threading.Thread(target=run_taipy)
#
#     flask_thread.start()
#     taipy_thread.start()
#
#     flask_thread.join()
#     taipy_thread.join()

###################################################

from flask import Flask
from taipy.gui import Gui
import multiprocessing

# Create the Flask app
app = Flask(__name__)

# Data to display in the chart
list_to_display = [100/x for x in range(1, 100)]

page = f"""
<|{{list_to_display}}|chart|>
"""

# Taipy GUI setup
taipy_page = Gui(page)

# Define the Flask route for the homepage
@app.route('/')
def index():
    return """
    <h1>Welcome to the Flask Homepage!</h1>
    <p><a href="http://localhost:5001/">Go to Taipy Page</a></p>
    """

# Function to run the Flask app
def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)

# Function to run the Taipy app
def run_taipy():
    taipy_page.run(port=5001, run_browser=False)  # Disable auto-launch of the browser

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

