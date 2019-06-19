from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/submit", methods=["POST"])
def submit():
    # Validate form submission - check that all the required 'name="xyz"' attributes are received. if not, redirect to error. (server-side)
    if not request.form.get("year"):
        return render_template("error.html", message="You failed to provide your name")
    if not request.form.get("question"):
        return render_template("error.html", message="You failed to provide your name")
    if not request.form.get("answer"):
        return render_template("error.html", message="You failed to provide your name")

