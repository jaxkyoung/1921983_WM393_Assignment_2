# encyption library
import bcrypt
from getpass import getpass

'''Class to create, read, update, verify, and delete user profiles'''
class boardAccess(object):

    # function to add user to json DB, requires valid email, password, first name and surname
    def addPendingUser(db, PendingUser, email, password, fName, sName, userType):
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

    # function to add user to json DB, requires valid email, password, first name and surname
    def addUser(db, User, email, password, fName, sName, userType):
        # hash the input password
        hash = userAccess.get_hashed_password(password)
        # convert hash to string
        hash = str(hash)
        # extract raw hash
        hash = hash.split("'")
        hash = hash[1]
        # form dictionary to be appended to json DB
        user = User(   
            email = email, 
            password = hash, 
            fName = fName, 
            sName = sName,
            userType = userType
        )
        db.session.add(user)
        db.session.commit()

    # returns list of users in user table
    def getUserDetails(User):
        users = User.query.all()
        return users
    
    # returns list of pending users in pendinguser table
    def getPendingUserDetails(PendingUser):
        users = PendingUser.query.all()
        return users

    # returns hashed password when plain text password is passed to it
    def get_hashed_password(plain_text_password):
        # Hash a password for the first time
        # (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())

    # returns boolena when passed with email and plain text password
    def check_password(User, email, plain_text_password):
        users = userAccess.getUserDetails(User)
        for user in users:
            if user.email == email:
                hashed_password = user.password
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

    def getUser(User, email):
        users = User.query.filter_by(email = email).first()
        return users

    def getUserName(User, email):
        users = userAccess.getUserDetails(User)
        # Iterating through the json user detials until matching details found
        for user in users:
            if user.email == email:
                return user.fName, user.sName

    def getUserType(User, email):
        users = userAccess.getUserDetails(User)
        # Iterating through the json user detials until matching details found
        for user in users:
            if user.email == email:
                return user.userType

    def approveUser(db, PendingUser, User, email):
        users = userAccess.getPendingUserDetails(PendingUser)
        for user in users:
            if user.email == email:
                user_to_approve = User(
                    email = user.email, 
                    password = user.password, 
                    fName = user.fName, 
                    sName = user.sName, 
                    userType = user.userType
                )
                db.session.delete(user)
                db.session.add(user_to_approve)
                db.session.commit()

    def denyUser(db, PendingUser, email):
        users = userAccess.getPendingUserDetails(PendingUser)
        for user in users:
            if user.email == email:
                db.session.delete(user)
                db.session.commit()

#userAccess.addPendingUser("john.smith@warwick.ac.uk", "example", "John", "Smith", "student")
# users = PendingUser.query.all()
# for user in users:
#     print(user.email)
