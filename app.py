from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    posts = Post.query.all()
    return render_template('index.html', posts=posts)
  else:
    content = request.form.get('content')
    due = request.form.get('due')
    
    due = datetime.strptime(due, '%Y-%m-%d')
    new_post = Post(content=content, due=due)
    
    db.session.add(new_post)
    db.session.commit()
    return redirect('/')
  
@app.route('/create')
def create():
  return render_template('create.html')

if __name__ == "__main__":
  app.run(debug=True)