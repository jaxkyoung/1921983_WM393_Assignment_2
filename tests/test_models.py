from app.models import db, User, Question, Answer, QABoard, PendingUser

def test_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password, first name and surname and role fields are defined correctly
    """
    new_user = User(
        email = 'test@test.co.uk', 
        password = 'test', 
        fName = 'firstNameTest', 
        sName = 'lastNameTest', 
        userType = 'Student'
    )
    assert new_user.email == 'test@test.co.uk'
    assert new_user.password == 'test'
    assert new_user.fName == 'firstNameTest'
    assert new_user.sName == 'lastNameTest'
    assert new_user.userType == 'Student'
    
    
def test_pending_user():
    """
    GIVEN a PendingUser model
    WHEN a new PendingUser is created
    THEN check the email, password, first name and surname and role fields are defined correctly
    """
    new_user = PendingUser(
        email = 'test@test.co.uk', 
        password = 'test', 
        fName = 'firstNameTest', 
        sName = 'lastNameTest', 
        userType = 'Student'
    )
    assert new_user.email == 'test@test.co.uk'
    assert new_user.password == 'test'
    assert new_user.fName == 'firstNameTest'
    assert new_user.sName == 'lastNameTest'
    assert new_user.userType == 'Student'
    
def test_QABoard():
	"""
	GIVEN a QABoard model
	WHEN a board is created
	THEN check the name, description, img path are correct
	"""
	new_board = QABoard(
		boardName = 'Test Board',
		boardDesc = 'Test Description'
	)
	assert new_board.boardName == 'Test Board'
	assert new_board.boardDesc == 'Test Description'
 

def test_question():
    date = "18/11/00"
    new_question = Question(
		qTitle = 'Test Title',
		qBody = 'Test Body',
		postDate = date,
		posterId = 1,
		boardId = 2
	)
    assert new_question.qTitle == 'Test Title'
    assert new_question.qBody == 'Test Body'
    assert new_question.postDate == '18/11/00'
    assert new_question.posterId == 1
    assert new_question.boardId == 2
    
def test_answer():
    pass
