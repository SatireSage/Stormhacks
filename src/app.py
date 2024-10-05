from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Index method for webpage

    Parameters:
        None

    Returns:
        render_template with the base index html page

    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
