import pytest
from app.main import app, db, User, Blog

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user
            user = User(username='testuser', password='testpass')
            db.session.add(user)
            db.session.commit()
        yield client

def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json['status'] == 'ok'

def test_login_success(client):
    res = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    assert res.status_code == 200
    assert 'Login successful' in res.json['message']

def test_login_failure(client):
    res = client.post('/login', json={'username': 'testuser', 'password': 'wrong'})
    assert res.status_code == 401

def test_blog_creation(client):
    # Login first
    login_res = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    assert login_res.status_code == 200

    # Create blog
    blog_res = client.post('/blog', json={'title': 'Test Blog', 'content': 'Hello World!'})
    assert blog_res.status_code == 200
    assert 'Blog posted' in blog_res.json['message']

def test_sql_injection_attempt(client):
    res = client.post('/login', json={'username': "' OR 1=1 --", 'password': 'any'})
    # This should fail — if it doesn't, the app is vulnerable
    assert res.status_code != 200
