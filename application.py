from flask import Flask, redirect, render_template, request, flash, url_for, jsonify
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
        return render_template('index.html', title="Check Solutions")
    if request.method == "POST":
        return render_template('index.html', year=request.form.get('year'),
                               question=request.form.get('question'),
                               answer=request.form.get('answer'),
                               response=request.form.get('response'))


@app.route("/form", methods=["POST"])
def submit():
    # Validate form submission server side - check that all the required 'name="xyz"' attributes
    # are received. if not, redirect to error. (server-side)
    print("in /form")
    if not request.form.get("year"):
        return render_template("error.html", message="You failed to provide a year")
    if not request.form.get("choosequestion"):
        return render_template("error.html", message="You failed to provide a question number")
    if not request.form.get("answer"):
        return render_template("error.html", message="You failed to provide an answer")

    year = request.form.get('year')
    question = request.form.get('choosequestion')
    answer = request.form.get('answer')
    # Check answer, using our check function in solutions.py.
    response = check(year, question, answer)
    if response == "correct":
        flash(f"Well done, you solved {year}'s Question #{question} - {answer} is correct!",
              'success')
        # do database thingies
    else:
        flash(f"Unfortunately, {answer} is not the correct answer for {year}'s Question\
              #{question}", 'danger')
    return redirect(url_for('index', year=year, question=question, answer=answer,
                    response=response), code=307)


@app.route("/puzzlepacks", methods=["GET"])
def puzzlepacks():
    return render_template('puzzlepacks.html', title="Downloads")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html", title="About")


@app.route("/checkJS", methods=["GET"])
def checkJS():
    """Destination of JavaScript request that checks answer. Returns true if answer available,
    else false, in JSON format"""
    # We have done this server-side in '/regiser'
    print("checkJS")
    year = request.args.get("year")
    question = request.args.get("question")
    answer = request.args.get("answer")
    print(f"answer in checkjs is {answer}")
    response = check(year, question, answer)
    if response == "correct":
        print("JS RIGHT!!!!!!!!!")
        return "true"  # Answer correct, form will submit + redirect to /form
    else:
        print("JS WRONG")
        return "false"  # Answer wrong, form will not submit.


# HTML FRAGMENT RETRIEVAL
@app.route("/2016", methods=["GET", "POST"])
def twentySixteen():
    if request.method == "GET":  # Return html form fragment to index
        return render_template('2016.html')


@app.route("/2017", methods=["GET", "POST"])
def twentySeventeen():
    if request.method == "GET":  # Return html form fragment to index
        return render_template('2017.html')


@app.route("/2018", methods=["GET", "POST"])
def twentyEighteen():
    if request.method == "GET":  # Return html form fragment to index
        return render_template('2018.html')


@app.route("/2019", methods=["GET", "POST"])
def twentyNineteen():
    if request.method == "GET":  # Return html form fragment to index
        return render_template('2019.html')
