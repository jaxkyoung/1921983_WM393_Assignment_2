from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import backref

db = SQLAlchemy()


# database table defnitions
# board table, to track Q&A boards
class QABoard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    boardName = db.Column(db.String(50), nullable = False)
    boardDesc = db.Column(db.String(500), nullable = True)
    backImg = db.Column(db.String(100), nullable = True)
    questions = db.relationship('Question', backref='board')

# user table, to track current registered users that have been approved
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    fName = db.Column(db.String(20), nullable = False)
    sName = db.Column(db.String(30), nullable = False)
    userType = db.Column(db.String(20), nullable = False)
    questions = db.relationship('Question', backref='author')
    answers = db.relationship('Answer', backref='author')
    comments = db.relationship('Comment', backref='author')

# pending user table, to track pending users waiting for access approval
class PendingUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    fName = db.Column(db.String(20), nullable = False)
    sName = db.Column(db.String(30), nullable = False)
    userType = db.Column(db.String(20), nullable = False)

# question table to track questions being asked on posts
# with foreign keys linking to users and boards
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    qTitle = db.Column(db.String(500), nullable = False)
    qBody = db.Column(db.String(1000))
    postDate = db.Column(db.DateTime)
    posterId = db.Column(db.Integer, db.ForeignKey(User.id))
    boardId = db.Column(db.Integer, db.ForeignKey(QABoard.id))
    answers = db.relationship('Answer', backref='question')
    comments = db.relationship('Comment', backref='question')

# answer table to track answers to questions from question tabel
# foreign keys linking to question and users
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    aBody = db.Column(db.String(2000))
    postDate = db.Column(db.DateTime)
    posterId = db.Column(db.Integer, db.ForeignKey(User.id))
    questionId = db.Column(db.Integer, db.ForeignKey(Question.id))
    
# comment table to track comments on questions from question tabel
# foreign keys linking to question and users
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cBody = db.Column(db.String(2000))
    postDate = db.Column(db.DateTime)
    posterId = db.Column(db.Integer, db.ForeignKey(User.id))
    questionId = db.Column(db.Integer, db.ForeignKey(Question.id))
