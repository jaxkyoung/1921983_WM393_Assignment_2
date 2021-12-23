'''
app.py contains all code that generates URLs for the flask web app, it depends on two supporting I/O handling python files:
    - dbBoardAccess.py (to access board, question, answer, and comment details)
    - dbUserAccess.py (to access user information for log in/out)
author: u1921983
version: 1.0
'''

'''Library imports'''
# file saving and path locating libraries
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename

# flask library for main website building
from flask import Flask

# flask library to generate url for function
from flask import url_for

# flask function to load jinja template
from flask import render_template

# for form processing
from flask import request

# for short term screen prompts/messages
from flask import flash

# flask library to redirect to another page
from flask import redirect

# flask libraries to handle user logins and account tracking
from flask_login import UserMixin, login_manager, login_user
from flask_login import LoginManager, login_required, logout_user, current_user

# SQLAlchemy for database creation and updating
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_migrate import Migrate

# class containing methods to access and write users to database
from app.dbUserAccess import userAccess
from app.dbBoardAccess import boardAccess


'''App initialisation'''
# initialising flask app and path to database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WMGTSS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import logging

app.logger.addHandler(logging.StreamHandler(os.system.stdout))
app.logger.setLevel(logging.ERROR)

'''Log-in manager initialisation'''
# initalising login manager
login_manager = LoginManager()
login_manager.init_app(app)
# link to log in page
login_manager.login_view = "logIn"


'''DB handling and table creation'''
# initialising database
db = SQLAlchemy(app)
# to handle adding or removing of columns of already created DB
migrate = Migrate(app, db)

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


''' Misc and Error Handling'''
# user loader to remember previously visited users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# error handler for 404 errors
@app.errorhandler(404)
def bar(error):
    # when 404 error, render error template
    return render_template('error.html'), 404


'''Home Page'''
# home page
@app.route('/home')
def goHome():
    return "Home"

# home page, containing default WMGTSS information
@app.route('/')
def home():
    # get first name to show in template
    return render_template('home.html')


'''Q&A board page, board creation and deletion'''
# Q&A board page
@app.route('/Q-A-Board')
@login_required
def QABoardHome():
    boards = boardAccess.getBoards(QABoard)
    return render_template('boards/q_a_board_home.html', boards=boards)

# Q&A board CRUD button processing
@app.route('/Q-A-Board', methods=['POST'])
def QABoard_post():
    if request.form['action'] == 'createBoardSubmit':
        boardName = request.form['boardName']
        boardDesc = request.form['boardDesc']
        f = request.files['imgPath']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        boardAccess.createBoard(db, QABoard, boardName, boardDesc, filename)
    if request.form['action'] == 'deleteBoardSubmit':
        boardId = request.form['boardId']
        boardAccess.deleteBoard(db, QABoard, boardId)
    if request.form['action'] == 'editBoardSubmit':
        pass
        # boardId = request.form['boardId']
        # boardName = request.form['boardName']
    return redirect(url_for('QABoardHome'))   

@app.route('/Q-A-Board/id/<boardId>')
@login_required
def QABoard_abstract(boardId):
    board = boardAccess.getBoard(QABoard, boardId)
    questions = boardAccess.getQuestions(Question, boardId)
    return render_template('boards/q_a_board_abstract.html', board=board, questions=questions)


'''Question, answer, and comment creation, deletion'''
# Question CRUD processing
@app.route('/Q-A-Board/id/<boardId>', methods=['POST'])
@login_required
def QABoard_abs_post(boardId):
    if request.form['action'] == 'askQuestionSubmit':
        board = boardAccess.getBoard(QABoard, boardId)
        questions = boardAccess.getQuestions(Question, boardId)
        qTitle = request.form['qTitle']
        qBody = request.form['qBody']
        boardAccess.addQuestion(db, Question, qTitle, qBody, boardId)
        return render_template('boards/q_a_board_abstract.html', board=board, questions=questions)
    if request.form['action'] == 'addAnswerSubmit':
        pass


'''User Log-in, Log-out, and approval pages'''
# log in page
@app.route('/log-in')
def logIn():
    # render logIn template 
    return render_template('auth/log-in.html', authError = False)

# function to handle login form POST request
@app.route('/log-in', methods=['POST'])
def logIn_post():
    # get email and password from form
    userEmail = request.form["userEmail"]
    userPassword = request.form["userPassword"]
    # check if password and email match database
    check = userAccess.check_password(User, userEmail, userPassword)
    # if check is true
    if check == True:
        # get user from db
        user = userAccess.getUser(User, userEmail)
        if user.email == userEmail:
            # log in user
            login_user(user)
        # return confirmation of login and redirect
        return 'You are logged in, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
    else:
        # if check is false, then user not logged in, flag error in password or email. 
        return render_template('auth/log-in.html', authError = True)

# log out page
@app.route('/logged-out/')
@login_required
def logOut():
    # flask function to logout user
    logout_user()
    # after being logged out, redirect in 3 seconds to home
    return 'You are logged out, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}

# forgot password page
@app.route('/forgotPasswordPage')
def forgotPasswordPage():
    #flash('Hello')
    return render_template('auth/forgotPassword.html', authError = False)

# create account page
@app.route('/create-account')
def register():
    # render create account page
    return render_template('auth/register.html')

# create account POST method form processing
@app.route('/create-account', methods=["POST"])
def register_post():
    # get form results
    userFirstNameInput = request.form["userFirstNameInput"]
    userSurnameInput = request.form["userSurnameInput"]
    userEmail = request.form["userEmail"]
    userPassword = request.form["userPassword"]
    userType = request.form["userType"]
    userPasswordRepeat = request.form["userPasswordRepeat"]

    # check user type and change to text
    if userType == "1":
        flash('Please select a user type')
        return render_template('auth/register.html')
    if userType == "2":
        userType = "Tutor"
    elif userType == "3":
        userType = "Teaching Assistant"
    elif userType == "4":
        userType = "Student"

    # if user password matches repeated password
    if userPassword == userPasswordRepeat:
        # AND email does not already exist
        notExists = db.session.query(User.id).filter_by(email=userEmail).first() is None
        if notExists:
            # if tutor or TA
            if userType == "Tutor" or userType == "Teaching Assistant":
                # add to pending users
                userAccess.addPendingUser(db, PendingUser, userEmail, userPassword, userFirstNameInput, userSurnameInput, userType)
                return 'You have created a privileged account with email: ' + userEmail + ', you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
            # if student, activate account immediately
            elif userType == "Student":
                userAccess.addUser(db, User, userEmail, userPassword, userFirstNameInput, userSurnameInput, userType)
                return 'You have created a standard account with email: ' + userEmail + ', you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
    else:
        flash('Passwords do not match', 'error')
        return render_template('auth/reigster.html')

# user approval page
@app.route('/approvals')
# login required for this page
@login_required
def approvalsPage():
    users = userAccess.getPendingUserDetails(PendingUser)
    if current_user.userType == "Tutor":
        return render_template('auth/approve_user.html', title='User Access Approvals', users=users)
    else:
        return "Student's arent allowed on this page"

# user approval processing
@app.route('/approvals/approve/<email>/')
def approveUser(email):
    users = userAccess.getPendingUserDetails(PendingUser)
    userAccess.approveUser(db, PendingUser, User, email)
    flash(email + ' shall be approved')
    return render_template('auth/approve_user.html', title='User Access Approvals', users=users)

# deny user processing
@app.route('/approvals/deny/<email>/')
def denyUser(email):
    users = userAccess.getPendingUserDetails(PendingUser)
    userAccess.denyUser(db, PendingUser, email)
    flash(email + ' shall be denied access')
    return render_template('auth/approve_user.html', title='User Access Approvals', users=users)


'''Flask App Initialisation'''
# run app
# if __name__ == '__main__':
#     app.secret_key = ('super secret key')
#     app.run(debug=True)