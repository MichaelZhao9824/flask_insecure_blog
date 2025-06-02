
from flask import Blueprint, render_template, request, redirect, session
from .models import db, Post

blog = Blueprint('blog', __name__)

@blog.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@blog.route('/create', methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect('/login')
    title = request.form['title']
    content = request.form['content']
    db.session.add(Post(title=title, content=content, author_id=session['user_id']))
    db.session.commit()
    return redirect('/')

@blog.route('/admin/exec')
def dangerous():
    return str(eval("2 + 2"))  # security issue!
