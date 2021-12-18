from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

# class containing methods to access and write users to database
from dbAccess import userAccess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WMGTSS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "logInReq"

db = SQLAlchemy(app)

# database table defnitions
class QABoard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    boardName = db.Column(db.String(50), nullable = False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    fName = db.Column(db.String(20), nullable = False)
    sName = db.Column(db.String(30), nullable = False)
    userType = db.Column(db.String(20), nullable = False)

class PendingUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    fName = db.Column(db.String(20), nullable = False)
    sName = db.Column(db.String(30), nullable = False)
    userType = db.Column(db.String(20), nullable = False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    qTitle = db.Column(db.String(500), nullable = False)
    qBody = db.Column(db.String(1000))
    postDate = db.Column(db.DateTime)
    posterId = db.Column(db.Integer, db.ForeignKey(User.id))
    boardId = db.Column(db.Integer, db.ForeignKey(QABoard.id))

posts = [
    { "title": "The answer for the Session 8 quiz is available on the Moodle", "name": "Young Park", "date": "20 Oct 2021", "count": 2 },
    { "title": "The answers for the quiz today is available on the Moodle", "name": "Young Park", "date": "19 Oct 2021", "count": 3 },
    { "title": "The Block 2 starts next week (18/10/21 - 21/10/21)", "name": "Alaa Sebae", "date": "12 Oct 2021", "count": 0 },
    { "title": "Unable to access library online resources", "name": "Alaa Sebae", "date": "28 Sep 2021", "count": 1 },
    { "title": "Task for finding functional and non-functional requirement available.", "name": "Young Park", "date": "17 Sep 2021", "count": 4 },
    { "title": "Welcome to WM393 module", "name": "Young Park", "date": "05 Sep 2021", "count": 8 }
]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    loggedIn = userAccess.isLoggedIn()
    userFirstName = userAccess.getUserFirstName(User, current_user)
    return render_template('home.html', title='Q&A Board', posts=posts, userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/logged-out/')
def logOut():
    logout_user()
    return 'You are logged out, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}

@app.route('/create-account')
def createAccountPage():
    loggedIn = userAccess.isLoggedIn()
    userFirstName = userAccess.getUserFirstName(User, current_user)
    return render_template('createAccount.html', userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/create-account', methods=["POST"])
def createAccount_post():
    userFirstNameInput = request.form["userFirstNameInput"]
    userSurnameInput = request.form["userSurnameInput"]
    userEmail = request.form["userEmail"]
    userPassword = request.form["userPassword"]
    userType = request.form["userType"]
    userPasswordRepeat = request.form["userPasswordRepeat"]

    if userType == "2":
        userType = "Tutor"
    elif userType == "3":
        userType = "Teaching Assistant"
    elif userType == "4":
        userType = "Student"

    print(userType)

    if userPassword == userPasswordRepeat:
        notExists = db.session.query(User.id).filter_by(email=userEmail).first() is None
        if notExists:
            if userType == "Tutor" or userType == "Teaching Assistant":
                userAccess.addPendingUser(db, PendingUser, userEmail, userPassword, userFirstNameInput, userSurnameInput, userType)
                return 'You have created a privileged account with email: ' + userEmail + ', you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
            elif userType == "Student":
                userAccess.addUser(db, User, userEmail, userPassword, userFirstNameInput, userSurnameInput, userType)
                return 'You have created a standard account with email: ' + userEmail + ', you will be redirected in 3 seconds', {"Refresh": "3; url = /"}

@app.route('/approvals')
@login_required
def approvalsPage():
    users = userAccess.getPendingUserDetails(PendingUser)
    loggedIn = userAccess.isLoggedIn()
    userFirstName = userAccess.getUserFirstName(User, current_user)
    return render_template('userApproval.html', title='User Access Approvals', users=users, userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/approvals/approve/<email>/')
def approveUser(email):
    loggedIn = userAccess.isLoggedIn()
    userFirstName = userAccess.getUserFirstName(User, current_user)
    users = userAccess.getPendingUserDetails(PendingUser)
    flash(email + ' shall be approved')
    return render_template('userApproval.html', title='User Access Approvals', users=users, userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/home')
def goHome():
    return "Home"

@app.route('/forgotPasswordPage')
def forgotPasswordPage():
    #flash('Hello')
    loggedIn = userAccess.isLoggedIn()
    userFirstName = userAccess.getUserFirstName(User, current_user)
    return render_template('forgotPassword.html', loggedIn = loggedIn, userFirstName = userFirstName, authError = False)


@app.route('/Q-A-Board')
@login_required
def QABoardHome():
    loggedIn = userAccess.isLoggedIn()
    userFirstName = userAccess.getUserFirstName(User, current_user)
    return render_template('QABoard.html', title='Q&A Board', posts=posts, userFirstName = userFirstName, loggedIn = loggedIn)

@app.route('/log-in')
def logInReq():
    loggedIn = userAccess.isLoggedIn()
    userFirstName = userAccess.getUserFirstName(User, current_user)
    return render_template('logIn2.html', loggedIn = loggedIn, userFirstName = userFirstName, authError = False)

@app.route('/log-in', methods=['POST'])
def logInReq_post():
    loggedIn = userAccess.isLoggedIn()
    userEmail = request.form["userEmail"]
    userPassword = request.form["userPassword"]
    check = userAccess.check_password(User, userEmail, userPassword)
    if check == True:
        users = userAccess.getUser(User, userEmail)
        for user in users:
            if user.email == userEmail:
                login_user(user)
        return 'You are logged in, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}
    else:
        userFirstName = ''
        return render_template('logIn2.html', loggedIn = loggedIn, userFirstName = userFirstName, authError = True)

if __name__ == '__main__':
    app.secret_key = ('super secret key')
    app.run(debug=True)

