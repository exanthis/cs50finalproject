from flask import Flask, redirect, render_template, request

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


@app.route("/form", methods=["POST"])
def submit():
    # Validate form submission server side - check that all the required 'name="xyz"' attributes
    # are received. if not, redirect to error. (server-side)
    if not request.form.get("year"):
        return render_template("error.html", message="You failed to provide a year")
    if not request.form.get("question"):
        return render_template("error.html", message="You failed to provide a question number")
    if not request.form.get("answer"):
        return render_template("error.html", message="You failed to provide an answer")

    # Redirect to the appropriate year
    year = "/" + request.form.get('year')
    return redirect(year)


@app.route("/2016", methods=["GET", "POST"])
def twentySixteen():
    if request.method == "GET":
        return render_template('2016.html')

    if request.method == "POST":
        return  # TODO


@app.route("/2017", methods=["GET", "POST"])
def twentySeventeen():
    if request.method == "GET":
        return render_template('2017.html')

    if request.method == "POST":
        return  # TODO


@app.route("/2018", methods=["GET", "POST"])
def twentyEighteen():
    if request.method == "GET":
        return render_template('2018.html')

    if request.method == "POST":
        return  # TODO


@app.route("/2019", methods=["GET", "POST"])
def twentyNineteen():
    if request.method == "GET":
        return render_template('2019.html')

    if request.method == "POST":
        return  # TODO
