def login(client, email, password):
    return client.post('/log-in', data=dict(
        userEmail=email,
        userPassword=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logged-out', follow_redirects=True)

def test_login_logout(app):
    client = app.test_client()
    """Make sure login and logout works."""
    email = 'tutor@warwick.ac.uk'
    password = 'tutor'

    resp = login(client, email, password)
    assert b'You are logged in' in resp.data

    resp = logout(client)
    assert b'You are logged out' in resp.data
    
    resp = login(client, f"{email}x", password)
    assert b'Incorrect Email or Password!' in resp.data

    resp = login(client, email, f'{password}x')
    assert b'Incorrect Email or Password!' in resp.data
    
    