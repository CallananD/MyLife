import calendar
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    deadline = db.Column(db.Date)

db.create_all()

@app.get("/")
def home():
    todo_list = db.session.query(Todo).all()
    return render_template("home.html",todo_list=todo_list)

@app.get("/todo")
def todo():
    todo_list = db.session.query(Todo).all()
    return render_template("base.html", todo_list=todo_list)

@app.post("/add")
def add():
    title = request.form.get("title")
    deadline = request.form.get("deadline")
    if len(deadline) > 0:
        new_todo = Todo(title=title, complete=False,
                    deadline=datetime(int(deadline[0:4]),int(deadline[5:7]),int(deadline[8:10])))
    else:
        new_todo = Todo(title=title, complete=False, deadline=None)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo"))

@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))

@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))

events = [{'todo': 'Test events','date':'2022-04-30'}]
@app.get("/calendar")
def my_calendar():
    events = []
    for event in db.session.query(Todo).all():
        if event.complete == False:
            events.append({'todo':event.title,'deadline':event.deadline})
    return render_template("calendar.html", events=events)