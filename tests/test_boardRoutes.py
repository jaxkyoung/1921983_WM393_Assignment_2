import json
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