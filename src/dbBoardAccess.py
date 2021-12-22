'''
This file allows app.py to communicate with the SQLite DB through defined functions,
restricting user access and keeping data secure. It specifically accesses boards, questions, answers, and comments
author: u1921983
version: 1.0
'''

# encyption library
from flask_login import current_user
from datetime import datetime

# datetime object containing current date and time
def getDateTime():
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return now

'''Class to create, read, update, verify, and delete user profiles'''
class boardAccess(object):

    # Function to create board
    def createBoard(db, QABoard, boardName, boardDesc, imgPath):
        # form board object with passed params
        new_board = QABoard(
            boardName = boardName,
            boardDesc = boardDesc,
            backImg = imgPath
        )
        # add new board to session
        db.session.add(new_board)
        # commit DB
        db.session.commit()

    # Function to delete board
    def deleteBoard(db, QABoard, boardId):
        # get board with passed ID
        board = QABoard.query.filter_by(id=boardId).first()
        # delete board
        db.session.delete(board)
        # commit DB
        db.session.commit
    
    # Function to get list of boards
    def getBoards(QABoard):
        # query all boards in QABoard
        boards = QABoard.query.all()
        # return list of boards
        return boards
    
    # Function to get individual board
    def getBoard(QABoard, boardId):
        # query QAboard table with passed ID
        board = QABoard.query.filter_by(id=boardId).first()
        # return queried board
        return board

    # Function to edit board
    def editBoard(db, QABoard, boardId, boardName):
        # get board from ID
        board = QABoard.query.filter_by(id=boardId).first()
        # updated board name
        board.boardName = boardName
        # commit DB
        db.session.commit()

    # Function to get list of questions on a board
    def getQuestions(Question, boardId):
        # query questions board with boardID param
        questions = Question.query.filter_by(boardId=boardId).all()
        # return questions list
        return questions

    # Function to add question to a board
    def addQuestion(db, Question, qTitle, qBody, boardId):
        # get current data and time
        now = getDateTime()
        # form question object with title, body etc...
        new_question = Question(
            qTitle = qTitle,
            qBody = qBody,
            postDate = now,
            posterId = current_user.id,
            boardId = boardId
        )
        # add question to session
        db.session.add(new_question)
        # commit DB
        db.session.commit()

    # Function to delete question
    def deleteQuestion(db, Question, questionId):
        # get question by id
        question = Question.query.filter_by(id=questionId).first()
        # delete question
        db.session.delete(question)
        # commit DB
        db.session.commit()

    # Function to add answer
    def addAnswer(db, Answer, aBody, questionId):
        # get current time/date
        now = getDateTime()
        # create new answer object with passed params
        new_answer = Answer(
            aBody = aBody,
            postDate = now,
            posterId = current_user.id,
            questionId = questionId
        )
        # add answer to session
        db.session.add(new_answer)
        # commit DB
        db.session.commit()
