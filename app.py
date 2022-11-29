from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(100), nullable=False)
  due= db.Column(db.DateTime, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == "GET":
    posts = Post.query.order_by(Post.due).all()
    return render_template('index.html', posts=posts)
  else:
    content = request.form.get('content')
    due = request.form.get('due')
    
    due = datetime.strptime(due,'%Y-%m-%d')
    
    new_post = Post(content=content, due=due)
    
    db.session.add(new_post)
    db.session.commit()
    return redirect('/')
  
@app.route('/create')
def create():
  return render_template('create.html')

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')
  
@app.route('/update/<int:id>', methods=['GET', 'POST'])

def update(id):
  post = Post.query.get(id)
  if request.method == 'GET':
    return render_template('update.html', post=post)
  else:
    post.content = request.form.get('content')
    post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')
    
    db.session.commit()
    return redirect('/')
  
if __name__ == "__main__":
  app.run(debug=True)