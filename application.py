import os
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from solutions import check
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

DATABASE_URL = os.environ['DATABASE_URL']

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'c3c622ac561c3a11930731cd3aa5ee35'

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# Login required stuff
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

from models import User, Questions, Questionnames
from forms import RegistrationForm, LoginForm


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/chad')
@login_required
def chad():
    return render_template('chad.html', title='CHAD!!!!!')


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        users_solved_problems = Questions.query.filter_by(user_id=user.id).all()
        if users_solved_problems:
            return render_template('index.html', title="Check Solutions",
                                   users_solved_problems=users_solved_problems)
        else:
            return render_template('index.html', title="Check Solutions")
    else:
        return render_template('index.html', title="Check Solutions")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('index'))
    form = RegistrationForm()
    # Did the form validate when submitted, POST request
    if form.validate_on_submit():
        # Add to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


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

    year = request.form.get('year')
    question = request.form.get('choosequestion')
    answer = request.form.get('answer')
    # Check answer, using our check function in solutions.py.
    response = check(year, question, answer)
    if response == "correct":
        if current_user.is_authenticated:
            # Find question_id from the Questionnames static table, to insert as foreign key in
            # Questions record
            questionAnswered = year + '-' + question
            question_row = Questionnames.query.filter_by(question_number=questionAnswered).first()
            question_id = question_row.question_id
            # Insert the solution into the Questions record, so user knows they've solved this one
            user = User.query.filter_by(email=current_user.email).first()
            already_solved = Questions.query.filter_by(user_id=user.id, question_id=question_id).first()
            if already_solved:
                flash(f"Well done, you solved {year}'s Question #{question} - {answer} is correct!\
                        But you've solved this one before!", 'info')
            else:  # Has not solved this puzzle yet
                this_solved = Questions(question_id=question_id, user_id=user.id)
                db.session.add(this_solved)
                db.session.commit()
                flash(f"Well done, you solved {year}'s Question #{question} - {answer} is correct!",
                      'success')
        else:
            flash(f"Well done, you solved {year}'s Question #{question} - {answer} is correct!",
                  'success')
    else:
        flash(f"Unfortunately, {answer} is not the correct answer for {year}'s Question\
              #{question}", 'danger')
    return redirect(url_for('index'))


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
