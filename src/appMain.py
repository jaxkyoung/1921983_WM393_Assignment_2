from flask import Flask
from flask import url_for
from flask import render_template

global loggedIn
loggedIn = False



app = Flask(__name__)

posts = [
    { "title": "The answer for the Session 8 quiz is available on the Moodle", "name": "Young Park", "date": "20 Oct 2021", "count": 2 },
    { "title": "The answers for the quiz today is available on the Moodle", "name": "Young Park", "date": "19 Oct 2021", "count": 3 },
    { "title": "The Block 2 starts next week (18/10/21 - 21/10/21)", "name": "Alaa Sebae", "date": "12 Oct 2021", "count": 0 },
    { "title": "Unable to access library online resources", "name": "Alaa Sebae", "date": "28 Sep 2021", "count": 1 },
    { "title": "Task for finding functional and non-functional requirement available.", "name": "Young Park", "date": "17 Sep 2021", "count": 4 },
    { "title": "Welcome to WM393 module", "name": "Young Park", "date": "05 Sep 2021", "count": 8 }
]

userFirstName = 'Jack'

@app.route('/')
def index():
    global loggedIn
    print(loggedIn)
    return render_template('home.html', title='Q&A Board', posts=posts, userFirstName = userFirstName, loggedIn = loggedIn)
    #return render_template('dashboard.html', title='Dashboard Board Title', posts=posts)

@app.route('/logged-out/')
def logOut():
    global loggedIn
    loggedIn = False
    print(loggedIn)
    return 'You are logged out, you will be redirected in 3 seconds', {"Refresh": "3; url = /"}

@app.route('/home')
def goHome():
    return "Hello World"

@app.route('/log-in')
def logInReq():
    global loggedIn
    loggedIn = True
    print(loggedIn)
    return 'Log In Page'
    #return render_template('logIn.html')

if __name__ == '__main__':
    app.run(debug=True)
