import json

def login(client, email, password):
    return client.post('/log-in', data=dict(
        userEmail=email,
        userPassword=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logged-out', follow_redirects=True)

def test_ping(app):
    client = app.test_client()
    resp = client.get('/ping')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'pong' in data['message']
    assert 'success' in data['status']
    
def test_home(app):
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200

def test_QABoardHome(app):
    client = app.test_client()
    resp = client.get('/Q-A-Board')
    assert b"Q&A Boards" not in resp.data
    assert resp.status_code == 302
    
    email = 'tutor@warwick.ac.uk'
    password = 'tutor'
    login(client, email, password)
    resp = client.get('/Q-A-Board')
    assert b"Q&A Boards" in resp.data
    assert resp.status_code == 200