import calendar
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
todo_db = SQLAlchemy(app)


class Todo(todo_db.Model):
    id = todo_db.Column(todo_db.Integer, primary_key=True)
    title = todo_db.Column(todo_db.String(100))
    complete = todo_db.Column(todo_db.Boolean)
    deadline = todo_db.Column(todo_db.Date)

todo_db.create_all()

@app.get("/")
def home():
    todo_list = todo_db.session.query(Todo).all()
    events = []
    for event in todo_list:
        if event.complete == False:
            events.append({'todo':event.title,'deadline':event.deadline})
    return render_template("home.html",todo_list=todo_list, events=events)

@app.get("/todo")
def todo():
    todo_list = todo_db.session.query(Todo).all()
    return render_template("todo.html", todo_list=todo_list)

@app.post("/add")
def add():
    title = request.form.get("title")
    deadline = request.form.get("deadline")
    if len(deadline) > 0:
        new_todo = Todo(title=title, complete=False,
                    deadline=datetime(int(deadline[0:4]),int(deadline[5:7]),int(deadline[8:10])))
    else:
        new_todo = Todo(title=title, complete=False, deadline=None)
    todo_db.session.add(new_todo)
    todo_db.session.commit()
    return redirect(url_for("todo"))

@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = todo_db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    todo_db.session.commit()
    return redirect(url_for("todo"))

@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = todo_db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo_db.session.delete(todo)
    todo_db.session.commit()
    return redirect(url_for("todo"))

events = [{'todo': 'Test events','date':'2022-04-30'}]
@app.get("/calendar")
def my_calendar():
    events = []
    for event in todo_db.session.query(Todo).all():
        if event.complete == False:
            events.append({'todo':event.title,'deadline':event.deadline})
    return render_template("calendar.html", events=events)