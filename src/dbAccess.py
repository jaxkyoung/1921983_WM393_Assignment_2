from appMain import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# encyption library
import bcrypt
from getpass import getpass

db = SQLAlchemy(app)

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



'''Class to create, read, update, verify, and delete user profiles'''
class userAccess(object):

    # function to add user to json DB, requires valid email, password, first name and surname
    def addPendingUser(email, password, fName, sName, userType):
        # hash the input password
        hash = userAccess.get_hashed_password(password)
        # convert hash to string
        hash = str(hash)
        # extract raw hash
        hash = hash.split("'")
        hash = hash[1]
        # form dictionary to be appended to json DB
        user = PendingUser(   
            email = email, 
            password = hash, 
            fName = fName, 
            sName = sName,
            userType = userType
        )
        db.session.add(user)
        db.session.commit()

    def getUserDetails():
        users = User.query.all()
        for user in users:
            print(user.email)
 
    def getPendingUserDetails():
        # Opening JSON file
        f = open('src/pending_users.json')
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        # Closing file
        f.close()
        # Iterating through the json user detials until matching details found
        return data

    def get_hashed_password(plain_text_password):
        # Hash a password for the first time
        # (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())

    def check_password(email, plain_text_password):
        data = userAccess.getUserDetails()
        for i in data:
            if i['email'] == email:
                hashed_password = i['hash']
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

    def checkUser(email, password):
        pass

    def getUserName(email):
        data = userAccess.getUserDetails()
        # Iterating through the json user detials until matching details found
        for i in data:
            if i['email'] == email:
                return i['fName'], i['sName']

    def getUserType(email):
        data = userAccess.getUserDetails()
        # Iterating through the json user detials until matching details found
        for i in data:
            if i['email'] == email:
                return i['user_type']

#userAccess.addPendingUser("john.smith@warwick.ac.uk", "example", "John", "Smith", "student")
# users = PendingUser.query.all()
# for user in users:
#     print(user.email)
