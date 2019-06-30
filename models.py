from application import db
from datetime import datetime
from flask_login import UserMixin


# @login_manager.user_loader
# def load_user(user_id):
   # return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # We'll use a 60 char hashing algorithm
    password = db.Column(db.String(60), nullable=False)
    # Lazy - defines when SQLAlchemy loads the data. True means it's
    # loaded as necessary in one go - we'll be able to use this post
    # attribute to get all posts by one individual user. It's not a column.
    # It's just an additional query running in the background to get all user
    # posts. Since we're referencing the post class itself, we use uppercase.
    questions = db.relationship('Questions', backref='solver', lazy=True)

    # Returns a printable representation of the given object. repr() computes
    # the “official” string representation of an object
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"


class Questions(db.Model):
    # A record of the questions solved for every user. Filter by user id and question number.
    # Add in each question as it gets solved.
    solved_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questionnames.question_id'))
    # Current time. Don't put parentheses - because we want to pass in the
    # function as the argument, and not the current time.
    date_solved = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    # The id of the user who authored the post. in the foreign key, we're
    # referencing the table/column name, so we use lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        # Since users will author posts, we need a one-to-many relationship.
        # One user = many posts. one post = one user only.
        return f"Questions('{self.user_id}', '{self.question_id}', '{self.date_solved}')"


class Questionnames(db.Model):
    # A static table, holding all question numbers and the name for that question (e.g. 'look up')
    question_id = db.Column(db.Integer, nullable=False, primary_key=True)
    question_number = db.Column(db.String(20), nullable=False, unique=True)
    question_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        # Since users will author posts, we need a one-to-many relationship.
        # One user = many posts. one post = one user only.
        return f"Questionnames('{self.question_number}', '{self.question_name}')"
