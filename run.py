
from flask import Flask
from app.models import db
from app.auth import auth
from app.blog import blog

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
app.register_blueprint(health, url_prefix='/health')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(blog)

if __name__ == '__main__':
    app.run(debug=True)
