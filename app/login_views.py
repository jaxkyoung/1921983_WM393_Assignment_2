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
from flask_login import login_manager, login_user
from flask_login import login_required, logout_user, current_user

# SQLAlchemy for database creation and updating
from flask_migrate import Migrate

# class containing methods to access and write users to database
from app.api.dbUserAccess import userAccess

from app.models import db, User

from flask import current_app, Blueprint
login = Blueprint('login', __name__)


'''User Log-in, Log-out, and approval pages'''
# log in page
@login.route('/log-in')
def logIn():
    # render logIn template 
    return render_template('auth/log-in.html', authError = False)

# function to handle login form POST request
@login.route('/log-in', methods=['POST'])
def logIn_post():
    # get email and password from form
    userEmail = request.form["userEmail"]
    userPassword = request.form["userPassword"]
    # check if password and email match database
    check = userAccess.check_password(userEmail, userPassword)
    # if check is true
    if check == True:
        # get user from db
        user = userAccess.getUser(userEmail)
        if user.email == userEmail:
            # log in user
            login_user(user)
        # return confirmation of login and redirect
        return 'You are logged in, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
    else:
        # if check is false, then user not logged in, flag error in password or email. 
        return render_template('auth/log-in.html', authError = True)

# log out page
@login.route('/logged-out/')
@login_required
def logOut():
    # flask function to logout user
    logout_user()
    # after being logged out, redirect in 3 seconds to home
    return 'You are logged out, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}

# forgot password page
@login.route('/forgotPasswordPage')
def forgotPasswordPage():
    #flash('Hello')
    return render_template('auth/forgotPassword.html', authError = False)

# create account page
@login.route('/create-account')
def register():
    # render create account page
    return render_template('auth/register.html')

# create account POST method form processing
@login.route('/create-account', methods=["POST"])
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
                userAccess.addPendingUser(userEmail, userPassword, userFirstNameInput, userSurnameInput, userType)
                return 'You have created a privileged account with email: ' + userEmail + ', you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
            # if student, activate account immediately
            elif userType == "Student":
                userAccess.addUser(userEmail, userPassword, userFirstNameInput, userSurnameInput, userType)
                return 'You have created a standard account with email: ' + userEmail + ', you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
        else:
            flash('This email is already in use, please choose another.')
    else:
        flash('Passwords do not match', 'error')
        return render_template('auth/reigster.html')