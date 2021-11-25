from flask import Flask
from flask import url_for
from flask import render_template


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
def index():
    return render_template('list.html', title='Q&A Board', posts=posts, imgPath = "resources/wmg-the-university-of-warwick-logo-vector.png")

if __name__ == '__main__':
    app.run(debug=True)
