import bcrypt
from getpass import getpass
import json

class userAccess(object):

    def get_hashed_password(plain_text_password):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())

    def check_password(plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password.encode(), hashed_password)

    def checkUser(email, password):
        pass

    def getUserName(email):
        # Opening JSON file
        f = open('src/user.json')
 
        # returns JSON object as
        # a dictionary
        data = json.load(f)
 
        # Iterating through the json user detials until matching details found
        for i in data['user_details']:
            if i['email'] == email:
                return i['fName'], i['sName']

        # Closing file
        f.close()