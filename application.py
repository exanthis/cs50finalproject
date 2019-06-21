from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from solutions import check

# Configure application
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/finaldb'
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy(app)


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')


@app.route("/form", methods=["POST"])
def submit():
    # Validate form submission server side - check that all the required 'name="xyz"' attributes
    # are received. if not, redirect to error. (server-side)
    if not request.form.get("year"):
        return render_template("error.html", message="You failed to provide a year")
    if not request.form.get("choosequestion"):
        return render_template("error.html", message="You failed to provide a question number")
    if not request.form.get("answer"):
        return render_template("error.html", message="You failed to provide an answer")

    # Redirect to the appropriate year
    year = "/" + request.form.get('year')
    # Redirecting with code 307 because the redirect function provided in Flask sends a 302
    # status code to the client by default, which is changed to GET by many browsers.
    # 307 was created to disambiguate between the two (307 = POST, 303 = GET)
    return redirect(year, code=307)


@app.route("/2016", methods=["GET", "POST"])
def twentySixteen():
    if request.method == "GET":  # Return html form fragment to index
        return render_template('2016.html')

    if request.method == "POST":
        # Check answer
        year = request.form.get('year')
        question = request.form.get('choosequestion')
        answer = request.form.get('answer').upper()
        response = check(year, question, answer)
        if response == "correct":
            flash('Well done, that was correct!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Unfortunately, that was not correct', 'danger')
            return redirect(url_for('index'))


@app.route("/2017", methods=["GET", "POST"])
def twentySeventeen():
    if request.method == "GET":  # Return html form fragment to index
        return render_template('2017.html')

    if request.method == "POST":
        # Check answer
        return "<p>hello</p>"


@app.route("/2018", methods=["GET", "POST"])
def twentyEighteen():
    if request.method == "GET":  # Return html form fragment to index
        return render_template('2018.html')

    if request.method == "POST":
        # Check answer
        return "<p>hello</p>"


@app.route("/2019", methods=["GET", "POST"])
def twentyNineteen():
    if request.method == "GET":  # Return html form fragment to index
        return render_template('2019.html')

    if request.method == "POST":
        # Check answer
        return "<p>hello</p>"
