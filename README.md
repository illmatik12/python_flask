# Test Flask
## 
```bash
pip3 install virtualenv 
virtualenv flask
```

## sample data create 
```python
from app import app, db, User, Post
db.create_all()

user = User(username='user', email='user@blog.com', password='password')
db.session.add(user)
db.session.commit()
post1 = Post(title='첫 번째 게시물', content='첫 번째 게시물 내용', author=user)
post2 = Post(title='두 번째 게시물', content='두 번째 게시물 내용', author=user)
db.session.add(post1)
db.session.add(post2)
db.session.commit()
```

### Run flask
```bash
python3 app.py
```