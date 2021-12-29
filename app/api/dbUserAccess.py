'''
This file allows app.py to communicate securely with the SQLite DB, 
it specifically accesses the user table.
author: u1921983
version: 1.0
'''

# encyption library
import bcrypt
from getpass import getpass

from app.models import db, User, PendingUser

'''Class to create, read, update, verify, and delete user profiles'''
class userAccess(object):

    # function to add user to json DB, requires valid email, password, first name and surname
    def addPendingUser(email, password, fName, sName, userType):
        """Function to add user to pendinguser table

        Args:
            db (object): Database object from app.py
            PendingUser (object): PendingUser table object from app.py
            email (string): Unique email of user
            password (string): plain text password
            fName (string): First Name
            sName (string): Surname
            userType (string): User level requested on sign-up
        """
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
    def addUser(email, password, fName, sName, userType):
        """Function to add user to user table

        Args:
            db (object): Database object from app.py
            User (object): User table object from app.py
            email (string): Unique email of user
            password (string): plain text password
            fName (string): First Name
            sName (string): Surname
            userType (string): User level requested on sign-up
        """
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
    def getUserDetails():
        """Returns list of users

        Args:
            User (object): User table object from app.py

        Returns:
            list: List of dicts of users, can be accessed by iterating users and using user.FieldName
        """
        users = User.query.all()
        return users
    
    # returns list of pending users in pendinguser table
    def getPendingUserDetails():
        """Returns list of pending users in PendingUser table

        Args:
            PendingUser (object): PendingUser table object from app.py

        Returns:
            list: List of dicts of users, can be accessed by iterating users and using user.FieldName
        """
        users = PendingUser.query.all()
        return users

    # returns hashed password when plain text password is passed to it
    def get_hashed_password(plain_text_password):
        """Function to return hash of input password

        Args:
            plain_text_password (string): Plain text password input by user

        Returns:
            string: Hashed password
        """
        # Hash a password for the first time
        # (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())

    # returns boolena when passed with email and plain text password
    def check_password(email, plain_text_password):
        """Function to check given password against hash in DB, returns boolean

        Args:
            User (object): User table object from app.py
            email (string): Email of user you want to check password of
            plain_text_password (string): Plain text password input by user

        Returns:
            boolean: True if password matches DB, False if not.
        """
        users = userAccess.getUserDetails()
        for user in users:
            if user.email == email:
                hashed_password = user.password
                # Check hashed password. Using bcrypt, the salt is saved into the hash itself
                return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())
        return False   

    # returns user record associated with email
    def getUser(email):
        """Function returns User object of given email

        Args:
            User (object): User table object from app.py
            email (string): Email of user you want to get

        Returns:
            dictionary: User object of given user
        """
        users = User.query.filter_by(email = email).first()
        return users

    # returns users first and surname when passed email
    def getUserName(email):
        """Function that returns first and surname of a given user by checking email

        Args:
            User (object): User table object from app.py
            email (string): Email of user you want to get names of
        Returns:
            list: [First name, Surname]
        """
        users = userAccess.getUserDetails()
        # Iterating through the json user detials until matching details found
        for user in users:
            if user.email == email:
                return user.fName, user.sName

    # returns user type of passed user email
    def getUserType(email):
        """Function that returns user type (level) for a given user email

        Args:
            User (object): User table object from app.py
            email (string): Email of user you want to check privileges of

        Returns:
            string: User type (Tutor, TA, or Student)
        """
        user = User.query.filter_by(email = email).first()
        return user.userType

    # returns nothing, function denies user registration, i.e. moves user from PendingUser -> to User table
    def approveUser(email):
        """Function approves user access, moves user from pending to active user table.

        Args:
            db (object): Database object from app.py
            PendingUser (object): PendingUser table object from app.py
            User (object): User table object from app.py
            email (string): Email of user you want to approve
        """
        users = userAccess.getPendingUserDetails()
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

    # returns nothing, function approves user, i.e. deletes user from PendingUser
    def denyUser(email):
        """Function denies user access, removes user from pending user table

        Args:
            db (object): Database object from app.py
            PendingUser (object): PendingUser table object from app.py
            email (string): Email of user you want to deny access
        """
        users = userAccess.getPendingUserDetails()
        for user in users:
            if user.email == email:
                db.session.delete(user)
                db.session.commit()