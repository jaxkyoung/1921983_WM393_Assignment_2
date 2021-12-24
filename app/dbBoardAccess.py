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
    """Function to get and return current date and time in format dd/mm/YY H:M:S

    Returns:
        Datetime: Current date and time
    """
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return now

'''Class to create, read, update, verify, and delete user profiles'''
class boardAccess(object):

    # Function to create board
    def createBoard(db, QABoard, boardName, boardDesc, imgPath):
        """Function to create Q&A Board

        Args:
            db (object): Database object from app.py
            QABoard (object): Q&A table object from app.py
            boardName (string): A name for the board, to be displayed on board
            boardDesc (string): A description of what will be discussed in this board
            imgPath (string): Path to the image that shall be used for the board's thumbnail
        """
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
        """Function to delete board from Q&A board page

        Args:
            db (object): Database object from app.py
            QABoard (object): Q&A table object from app.py
            boardId (integer): Unique identifier for board that is going to be deleted
        """
        # get board with passed ID
        board = QABoard.query.filter_by(id=boardId).first()
        # delete board
        db.session.delete(board)
        # commit DB
        db.session.commit
    
    # Function to get list of boards
    def getBoards(QABoard):
        """Function to get list of current boards in DB

        Args:
            QABoard (object): Q&A table object from app.py

        Returns:
            list: DB records list of dictionaries of current boards in DB, fields can be accessed using the following syntax: board.FieldName
        """
        # query all boards in QABoard
        boards = QABoard.query.all()
        # return list of boards
        return boards
    
    # Function to get individual board
    def getBoard(QABoard, boardId):
        """Function to get fields of individual board

        Args:
            QABoard (object): Q&A table object from app.py
            boardId (integer): Unique identifier for board that is going to be accessed

        Returns:
            dictionary: Board with ID(boardId) is returned, can be accessed using board.FieldName
        """
        # query QAboard table with passed ID
        board = QABoard.query.filter_by(id=boardId).first()
        # return queried board
        return board

    # Function to edit board
    def editBoard(db, QABoard, boardId, boardName):
        """Function to edit board name and description

        Args:
            db (object): Database object from app.py
            QABoard (object): Q&A table object from app.py
            boardId (integer): Unique identifier for board that is going to be accessed
            boardName (string): A name for the board, to be displayed on board
        """
        # get board from ID
        board = QABoard.query.filter_by(id=boardId).first()
        # updated board name
        board.boardName = boardName
        # commit DB
        db.session.commit()

    # Function to get list of questions on a board
    def getQuestions(Question, boardId):
        """Function to get list of questions on given board

        Args:
            Question (object): DB Question table object
            boardId (integer): Unique identifier for board you want to get questions from

        Returns:
            list: DB records list of dictionaries of current questions in DB, fields can be accessed using the following syntax: question.FieldName
        """
        # query questions board with boardID param
        questions = Question.query.filter_by(boardId=boardId).all()
        # return questions list
        return questions

    # Function to add question to a board
    def addQuestion(db, Question, qTitle, qBody, boardId):
        """Function to add question to board

        Args:
            db (object): Database object from app.py
            Question (object): DB Question table object
            qTitle (string): Title of question to be shown on board
            qBody (string): Body of question to be shown on board
            boardId (integer): Unique identifier for board you want to add questions to
        """
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
        """Function to delete chosen question from questionId

        Args:
            db (object): Database object from app.py
            Question (object): DB Question table object
            questionId (integer): Unique identifier for question
        """
        # get question by id
        question = Question.query.filter_by(id=questionId).first()
        # delete question
        db.session.delete(question)
        # commit DB
        db.session.commit()

    # Function to add answer
    def addAnswer(db, Answer, aBody, questionId):
        """[summary]

        Args:
            db (object): Database object from app.py
            Answer (object): DB Answer table object
            aBody (string): Body of answer
            questionId (integer): Unique identifier for question
        """
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
    
    def getAnswers(Answer, boardId):
        """

        Args:
            Answer ([type]): [description]
        """
        #answers = Answer.query.filter_by(Answer.question.has(boardId==boardId))
        answers = Answer.query.join(Answer.question, aliased=True).filter_by(boardId=boardId)
        return answers