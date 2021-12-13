# encyption library
import bcrypt
from getpass import getpass
# json handling library
import json

'''Class to create, read, update, verify, and delete user profiles'''
class userAccess(object):

    # function to add user to json DB, requires valid email, password, first name and surname
    def addUser(email, password, fName, sName):
        # hash the input password
        hash = userAccess.get_hashed_password(password)
        # convert hash to string
        hash = str(hash)
        # extract raw hash
        hash = hash.split("'")
        hash = hash[1]
        # form dictionary to be appended to json DB
        userEntry = {   
            "email": email, 
            "fName": fName, 
            "sName": sName, 
            "hash": hash
        }
        # get current DB file
        data = userAccess.getUserDetails()
        # append added user
        data['user_details'].append(userEntry)
        with open('src/user.json', "w") as file:
            # write new DB to file with indent formatted
            json.dump(data, file, indent=4)

    def getUserDetails():
        # Opening JSON file
        f = open('src/user.json')
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
        for i in data['user_details']:
            if i['email'] == email:
                hashed_password = i['hash']
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

    def checkUser(email, password):
        pass

    def getUserName(email):
        data = userAccess.getUserDetails()
        # Iterating through the json user detials until matching details found
        for i in data['user_details']:
            if i['email'] == email:
                return i['fName'], i['sName']