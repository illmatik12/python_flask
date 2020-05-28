'''
from flask import Flask 
app = Flask(__name__)

@app.route("/")
def hello():
    val = "hello, world!"
    return val

https://opentutorials.org/module/3669/22003
'''

from datetime import datetime


from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app.config['SECRET_KEY'] = 'this is secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

api = Api(app)


'''
user = User(username='user', email='user@blog.com', password='password')
db.session.add(user)
db.session.commit()
post1 = Post(title='첫 번째 게시물', content='첫 번째 게시물 내용', author=user)
post2 = Post(title='두 번째 게시물', content='두 번째 게시물 내용', author=user)
db.session.add(post1)
db.session.add(post2)
db.session.commit()
'''

class SayHello(Resource):
    def get(self):
        return {'message': 'hello, world'}

class User(db.Model):
    __table_name__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_image = db.Column(db.String(100), default='default.png')

    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, username, email, password, **kwargs):
        self.username = username
        self.email = email

        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)
 
    def __repr__(self):
        return f"<User('{self.id}', '{self.username}', '{self.email}')>"

class Post(db.Model):
    __table_name__ = 'post'
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
    def __repr__(self):
        return f"<Post('{self.id}', '{self.title}')>"

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

#api
api.add_resource(SayHello, '/hello')

if __name__ == '__main__':
    app.run(debug=True)
