from flask import Flask, render_template, request, redirect, url_for
from flask import session as flask_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
import uuid
from setup_db import User, Task, Group
import datetime

#Initialisation
app = Flask(__name__)
app.secret_key = '0f71536e0640da386f0537f1'

engine = create_engine('sqlite:///userdata.db')
Session = sessionmaker(bind=engine)
session = Session()
# There are two types of sessions in this project: 
# flask_session from flask (renamed to avoid conflict) and session from sqlalchemy
# flask_session is used to store the user's session data, while session from sqlalchemy is used to interact with the database

#Welcome page when not signed in
@app.route('/')
def home():
    return render_template('index.html')


#Login/signup pages

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

# Submit signup details
@app.route('/signup', methods=['POST'])
def submitSignup():
    # Get the form data
    username = request.form['username-signup']
    password = request.form['password-signup']
    password_confirm = request.form['password-confirm']
    errors = []

    # Check for errors in the form data
    if username == '' or password == '' or password_confirm == '':
        errors.append('empty_field')
    elif len(password) < 8:
        errors.append('password_length')
    
    if password != password_confirm:
        errors.append('match_password')


    users = session.query(User).filter(User.username == username).all()
    if len(users) > 0:
        errors.append('username_taken')

    

    if len(errors) > 0:
        return render_template('signup.html', errors=errors)
    else:
        unique_id = str(uuid.uuid4())#gives each user a unique uuid

        user = User(id=unique_id, username=username, password=generate_password_hash(password))
        session.add(user)

        # Default groups for each user
        session.add(Group(user_id=unique_id, group_name='Personal', group_id=str(uuid.uuid4())))
        session.add(Group(user_id=unique_id, group_name='School', group_id=str(uuid.uuid4())))
        session.commit()

        
        flask_session['userId'] = user.id
        flask_session['username'] = user.username
        return redirect(url_for('dashboard'))
        
        
        

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html',failed_attempt=False)

@app.route('/login', methods=['POST'])
def submitLogin():
    # Get the form data
    username = request.form['username-login']
    password = request.form['password-login']

    # Check if the form data is empty
    if username == '' or password == '':
        return render_template("login.html",failed_attempt=True)

    # Check if the user exists
    user = session.query(User).filter(User.username == username).first()
    if user and user.check_password(password):
        # Set the session variables
        flask_session['userId'] = user.id
        flask_session['username'] = user.username
        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html",failed_attempt=True)
        
    


#Main page after login
@app.route('/dashboard')
def dashboard():
    userId = flask_session.get('userId')
    if userId is None:
        return redirect(url_for('login'))
    else:
        tasks = session.query(Task).filter(Task.user_id == userId).order_by(Task.due_date).all()

        groups = session.query(Group).filter(Group.user_id == userId).all()

        return render_template('dashboard.html', tasks=tasks, groups=groups)

# Registering a task as complete
@app.route('/complete', methods=['POST'])
def completeTask():
    task_id = request.form['task_id']
    task = session.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.completed = True
        session.commit()

    return redirect(url_for('dashboard'))

# Load the add task page
@app.route('/addtask', methods=['GET'])
def addtask():
    groups = session.query(Group).filter(Group.user_id == flask_session.get('userId')).all()

    return render_template('add_task.html',groups=groups)

# Submitting a new task
@app.route('/addtask', methods=['POST'])
def submitTask():
    errors = []

    # Get the form data
    task = request.form['task']

    if request.form['group-select'] != 'new':
        groupId = request.form['group-select']
        group = session.query(Group).filter(Group.group_id == groupId).first()
        
    else:
        new_group_name = request.form['new-group-input']
        new_group = Group(user_id=userId, group_name=new_group_name, group_id=str(uuid.uuid4()))
        session.add(new_group)
        session.commit()
        group = new_group

    details = request.form['description']

    due_date = request.form['due-date']
    if due_date == '':
        errors.append('empty_field')
    due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d')

    if request.form.get('important') == 'on':
        important = True
    else:
        important = False
    
    userId = flask_session.get('userId')

    # Check for errors in the form data
    if task == '':
        errors.append('empty_field')
    
    if len(errors) > 0:
        groups = session.query(Group).filter(Group.user_id == flask_session.get('userId')).all()
        return render_template('add_task.html', errors=errors,groups=groups)
    else:
        group_id = session.query(Group).filter(Group.group_name == group.group_name and Group.user_id == userId).first().group_id

        task = Task(user_id=userId, task_id=str(uuid.uuid4()), name=task, details=details, group_id=group_id, important=important, due_date=due_date, completed=False)
        session.add(task)
        session.commit()

        return redirect(url_for('dashboard'))

#View specific group
@app.route('/group/<group_id>')
def viewGroup(group_id):
    group = session.query(Group).filter(Group.group_id == group_id).first()
    tasks = session.query(Task).filter(Task.group_id == group_id).order_by(Task.due_date).all()

    return render_template('group.html', group=group, tasks=tasks)



app.run(debug=True, reloader_type='stat', port=5000)