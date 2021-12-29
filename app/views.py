'''
app.py contains all code that generates URLs for the flask web app, it depends on two supporting I/O handling python files:
    - dbBoardAccess.py (to access board, question, answer, and comment details)
    - dbUserAccess.py (to access user information for log in/out)
author: u1921983
version: 1.0
'''

'''Library imports'''
# file saving and path locating libraries
import os
from werkzeug.utils import secure_filename

# flask library to generate url for function
from flask import url_for

# flask function to load jinja template
from flask import render_template

# for form processing
from flask import request

# for short term screen prompts/messages
from flask import flash

# flask library to redirect to another page
from flask import redirect

# flask libraries to handle user logins and account tracking
from flask_login import login_required, logout_user

# class containing methods to access and write users to database
from app.api.dbBoardAccess import boardAccess

from flask import current_app

from flask import current_app, Blueprint, render_template
base = Blueprint('base', __name__)

# error handler for 404 errors
@base.errorhandler(404)
def bar(error):
    # when 404 error, render error template
    return render_template('error.html'), 404


'''Home Page'''
# home page
@base.route('/home')
def goHome():
    return "Home"

# home page, containing default WMGTSS information
@base.route('/')
def home():
    # get first name to show in template
    return render_template('home.html')


'''Q&A board page, board creation and deletion'''
# Q&A board page
@base.route('/Q-A-Board')
@login_required
def QABoardHome():
    boards = boardAccess.getBoards()
    return render_template('boards/q_a_board_home.html', boards=boards)

# Q&A board CRUD button processing
@base.route('/Q-A-Board', methods=['POST'])
def QABoard_post():
    if request.form['action'] == 'createBoardSubmit':
        boardName = request.form['boardName']
        boardDesc = request.form['boardDesc']
        f = request.files['imgPath']
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        boardAccess.createBoard(boardName, boardDesc, filename)
    if request.form['action'] == 'deleteBoardSubmit':
        boardId = request.form['boardId']
        boardAccess.deleteBoard(boardId)
    if request.form['action'] == 'editBoardSubmit':
        pass
        # boardId = request.form['boardId']
        # boardName = request.form['boardName']
    return redirect(url_for('base.QABoardHome'))   

@base.route('/Q-A-Board/id/<boardId>')
@login_required
def QABoard_abstract(boardId):
    board = boardAccess.getBoard(boardId)
    questions = boardAccess.getQuestions(boardId)
    answers = boardAccess.getAnswers(boardId)
    return render_template('boards/q_a_board_abstract.html', board=board, questions=questions, answers=answers)


'''Question, answer, and comment creation, deletion'''
# Question CRUD processing
@base.route('/Q-A-Board/id/<boardId>', methods=['POST'])
@login_required
def QABoard_abs_post(boardId):
    if request.form['action'] == 'askQuestionSubmit':
        qTitle = request.form['qTitle']
        qBody = request.form['qBody']
        boardAccess.addQuestion(qTitle, qBody, boardId)
    elif request.form['action'] == 'addAnswerSubmit':
        aBody = request.form['aBody']
        questionId = request.form['questionId']
        boardAccess.addAnswer(aBody, questionId)
    board = boardAccess.getBoard(boardId)
    questions = boardAccess.getQuestions(boardId)
    answers = boardAccess.getAnswers(boardId)
    return render_template('boards/q_a_board_abstract.html', board=board, questions=questions, answers=answers)

'''Search Functionality'''
@base.route('/results', methods=['POST'])
@login_required
def searchResults():
    if request.form['action'] == 'searchSubmit':
        search = request.form['search']
        boardResults = boardAccess.searchBoard(search)
        questionResults = boardAccess.searchQuestion(search)
        return render_template('search.html', questions=questionResults, boards=boardResults)

