from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from userAuth import userAccess

global userFirstName
global loggedIn
loggedIn = False
userFirstName = ''

app = Flask(__name__)

posts = [
    { "title": "The answer for the Session 8 quiz is available on the Moodle", "name": "Young Park", "date": "20 Oct 2021", "count": 2 },
    { "title": "The answers for the quiz today is available on the Moodle", "name": "Young Park", "date": "19 Oct 2021", "count": 3 },
    { "title": "The Block 2 starts next week (18/10/21 - 21/10/21)", "name": "Alaa Sebae", "date": "12 Oct 2021", "count": 0 },
    { "title": "Unable to access library online resources", "name": "Alaa Sebae", "date": "28 Sep 2021", "count": 1 },
    { "title": "Task for finding functional and non-functional requirement available.", "name": "Young Park", "date": "17 Sep 2021", "count": 4 },
    { "title": "Welcome to WM393 module", "name": "Young Park", "date": "05 Sep 2021", "count": 8 }
]

@app.route('/')
def home():
    global loggedIn
    print(loggedIn)
    return render_template('home.html', title='Q&A Board', posts=posts, userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/logged-out/')
def logOut():
    global loggedIn
    loggedIn = False
    return 'You are logged out, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}

@app.route('/create-account')
def createAccountPage():
    return render_template('createAccount.html', userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/create-account', methods=["POST"])
def createAccount_post():
    userFirstNameInput = request.form["userFirstNameInput"]
    userSurnameInput = request.form["userSurnameInput"]
    userEmail = request.form["userEmail"]
    userPassword = request.form["userPassword"]
    userType = request.form["userType"]
    return " " + userFirstNameInput + userSurnameInput + userEmail + userPassword + userType

@app.route('/approvals')
def approvalsPage():
    users = userAccess.getPendingUserDetails()
    return render_template('userApproval.html', title='User Access Approvals', users=users, userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/approvals/approve/<email>/')
def approveUser(email):
    users = userAccess.getPendingUserDetails()
    flash(email + ' shall be approved')
    return render_template('userApproval.html', title='User Access Approvals', users=users, userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/home')
def goHome():
    return "Home"

@app.route('/forgotPasswordPage')
def forgotPasswordPage():
    #flash('Hello')
    return render_template('forgotPassword.html', loggedIn = loggedIn, userFirstName = userFirstName, authError = False)


@app.route('/Q-A-Board')
def QABoardHome():
    global loggedIn
    if loggedIn == True:
        return render_template('QABoard.html', title='Q&A Board', posts=posts, userFirstName = userFirstName, loggedIn = loggedIn)
    else:
        return render_template('AccessError.html')

@app.route('/log-in')
def logInReq():
    return render_template('logIn2.html', loggedIn = loggedIn, userFirstName = userFirstName, authError = False)

@app.route('/log-in', methods=['POST'])
def logInReq_post():
    global loggedIn
    global userFirstName
    userEmail = request.form["userEmail"]
    userPassword = request.form["userPassword"]
    check = userAccess.check_password(userEmail, userPassword)
    if check == True:
        userNames = userAccess.getUserName(userEmail)
        userFirstName = userNames[0]
        loggedIn = True
        return 'You are logged in, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
    else:
        userFirstName = ''
        return render_template('logIn2.html', loggedIn = loggedIn, userFirstName = userFirstName, authError = True)

if __name__ == '__main__':
    app.secret_key = ('super secret key')
    app.run(debug=True)

