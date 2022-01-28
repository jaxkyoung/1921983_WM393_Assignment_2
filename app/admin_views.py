'''
app.py contains all code that generates URLs for the flask web app, it depends on two supporting I/O handling python files:
    - dbBoardAccess.py (to access board, question, answer, and comment details)
    - dbUserAccess.py (to access user information for log in/out)
author: u1921983
version: 1.0
'''

'''Library imports'''

# flask function to load jinja template
from flask import render_template

# for short term screen prompts/messages
from flask import flash

# flask libraries to handle user logins and account tracking
from flask_login import login_required, current_user

# class containing methods to access and write users to database
from app.api.dbUserAccess import userAccess

from flask import current_app, Blueprint, render_template
admin = Blueprint('admin', __name__)

# user approval page
@admin.route('/approvals')
# login required for this page
@login_required
def approvalsPage():
    users = userAccess.getPendingUserDetails()
    if current_user.userType == "Tutor":
        return render_template('auth/approve_user.html', title='User Access Approvals', users=users)
    else:
        return "Student's arent allowed on this page"

# user approval processing
@admin.route('/approvals/approve/<email>/')
def approveUser(email):
    users = userAccess.getPendingUserDetails()
    userAccess.approveUser(email)
    flash(email + ' shall be approved')
    return render_template('auth/approve_user.html', title='User Access Approvals', users=users)

# deny user processing
@admin.route('/approvals/deny/<email>/')
def denyUser(email):
    users = userAccess.getPendingUserDetails()
    userAccess.denyUser(email)
    flash(email + ' shall be denied access')
    return render_template('auth/approve_user.html', title='User Access Approvals', users=users)