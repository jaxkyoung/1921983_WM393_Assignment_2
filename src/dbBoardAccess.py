# encyption library
import bcrypt
from getpass import getpass
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

    def createBoard(db, QABoard, boardName):
        new_board = QABoard(
            boardName = boardName
        )
        db.session.add(new_board)
        db.session.commit()

    def deleteBoard(db, QABoard, boardId):
        board = QABoard.query.filter_by(id=boardId).first()
        db.session.delete(board)
        db.session.commit()
    
    def getBoards(QABoard):
        boards = QABoard.query.all()
        return boards

    def editBoard(db, QABoard, boardId, boardName):
        board = QABoard.query.filter_by(id=boardId).first()
        board.boardName = boardName
        db.session.commit()

    def addQuestion(db, Question, qTitle, qBody, boardId, posterId=current_user.id):
        now = getDateTime()
        new_question = Question(
            qTitle = qTitle,
            qBody = qBody,
            postDate = now,
            posterId = posterId,
            boardId = boardId
        )
        db.session.add(new_question)
        db.session.commit()

    def deleteQuestion(db, Question, questionId):
        question = Question.query.filter_by(id=questionId).first()
        db.session.delete(question)
        db.session.commit()

    def addAnswer(db, Answer, aBody, questionId, posterId=current_user.id):
        now = getDateTime()
        new_answer = Answer(
            aBody = aBody,
            postDate = now,
            posterId = posterId,
            questionId = questionId
        )
        db.session.add(new_answer)
        db.session.commit()
        