from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as flaskSession
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
sessionDb = Session()
# There are two types of sessions in this project: 
# flaskSession from flask (renamed to avoid conflict) and sessionDb is from sqlalchemy
# flaskSession is used to store the user's session data, while sessionDb is used to interact with the database.

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


    users = sessionDb.query(User).filter(User.username == username).all()
    if len(users) > 0:
        errors.append('username_taken')

    

    if len(errors) > 0:
        return render_template('signup.html', errors=errors)
    else:
        unique_id = str(uuid.uuid4())#gives each user a unique uuid

        user = User(id=unique_id, username=username, password=generate_password_hash(password))
        sessionDb.add(user)

        # Default groups for each user
        sessionDb.add(Group(user_id=unique_id, group_name='Personal', group_id=str(uuid.uuid4())))
        sessionDb.add(Group(user_id=unique_id, group_name='School', group_id=str(uuid.uuid4())))
        sessionDb.commit()

        
        flaskSession['userId'] = user.id
        flaskSession['username'] = user.username
        flaskSession['hideCompleted'] = False
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
    user = sessionDb.query(User).filter(User.username == username).first()
    if user and user.check_password(password):
        # Set the session variables
        flaskSession['userId'] = user.id
        flaskSession['username'] = user.username
        flaskSession['hideCompleted'] = False
        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html",failed_attempt=True)
        
    

#Main page after login
@app.route('/dashboard')
def dashboard():
    userId = flaskSession.get('userId')
    if userId is None:
        return redirect(url_for('login'))
    else:
        #Detects if completed tasks should be hidden
        hideCompleted = flaskSession.get('hideCompleted')

        if hideCompleted:
            tasks = sessionDb.query(Task).filter(Task.user_id == userId, Task.completed == False).order_by(Task.due_date).all()
        else:
            tasks = sessionDb.query(Task).filter(Task.user_id == userId).order_by(Task.due_date).all()

        groups = sessionDb.query(Group).filter(Group.user_id == userId).all()

        return render_template('dashboard.html', tasks=tasks, groups=groups, showDetails=False, hideCompleted=hideCompleted)

# Registering a task as complete
@app.route('/complete', methods=['POST'])
def completeTask():
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    task_id = request.form['task_id']
    task = sessionDb.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.completed = True
        sessionDb.commit()

    flash('Task Complete!')
    return redirect(url_for('dashboard'))

# De-complete-ify a task
@app.route('/decomplete', methods=['POST'])
def decompleteTask():
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    task_id = request.form['task_id']
    task = sessionDb.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.completed = False
        sessionDb.commit()

    return redirect(url_for('dashboard'))

# Load the add task page
@app.route('/addtask', methods=['GET'])
def addtask():
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    groups = sessionDb.query(Group).filter(Group.user_id == flaskSession.get('userId')).all()
    return render_template('add_task.html',groups=groups)

# Submitting a new task
@app.route('/addtask', methods=['POST'])
def submitTask():
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    errors = []

    # Get the form data
    task = request.form['task']

    userId = flaskSession.get('userId')

    if request.form['group-select'] != 'new':
        groupId = request.form['group-select']
        group = sessionDb.query(Group).filter(Group.group_id == groupId).first()
        
    else:
        new_group_name = request.form['new-group-input']
        if len(new_group_name) < 50 and new_group_name != '': # Group name must be less than 50 characters
            new_group = Group(user_id=userId, group_name=new_group_name, group_id=str(uuid.uuid4()))
            sessionDb.add(new_group)
            sessionDb.commit()
            group = new_group
        else:
            errors.append('group_name_length')

    details = request.form['description']

    dueDate = request.form['due-date']
    if dueDate == '':
        errors.append('empty_field')
    dueDate = datetime.datetime.strptime(dueDate, '%Y-%m-%d').date()

    if request.form.get('important') == 'on':
        important = True
    else:
        important = False

    # Check for errors in the form data
    if task == '':
        errors.append('empty_field')
    
    if len(errors) > 0:
        groups = sessionDb.query(Group).filter(Group.user_id == flaskSession.get('userId')).all()
        return render_template('add_task.html', errors=errors,groups=groups)
    else:
        group_id = sessionDb.query(Group).filter(Group.group_name == group.group_name and Group.user_id == userId).first().group_id

        task = Task(user_id=userId, task_id=str(uuid.uuid4()), name=task, details=details, group_id=group_id, important=important, due_date=dueDate, completed=False)
        sessionDb.add(task)
        sessionDb.commit()

        flash('Task added successfully!')
        return redirect(url_for('dashboard'))

#View specific group
@app.route('/group/<group_id>')
def viewGroup(group_id):
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    group = sessionDb.query(Group).filter(Group.group_id == group_id).first()
    tasks = sessionDb.query(Task).filter(Task.group_id == group_id).order_by(Task.due_date).all()

    return render_template('group.html', group=group, tasks=tasks, showDetails=True)

# View task details
@app.route('/task/<task_id>')
def viewTask(task_id):
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    task = sessionDb.query(Task).filter(Task.task_id == task_id).first()
    group = sessionDb.query(Group).filter(Group.group_id == task.group_id).first()

    return render_template('task.html', task=task, group=group)

# Edit task details
@app.route('/edittask/<task_id>', methods=['GET'])
def editTask(task_id):
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    task = sessionDb.query(Task).filter(Task.task_id == task_id).first()
    groups = sessionDb.query(Group).filter(Group.user_id == flaskSession.get('userId')).all()

    return render_template('edit_task.html', task=task, groups=groups)

# Submit edited task details
@app.route('/edittask/<task_id>', methods=['POST'])
def submitTaskEdit(task_id):
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    errors = []

    # Get the form data
    name = request.form['name']
    details = request.form['details']
    # group = request.form['group']
    dueDate = request.form['due_date']

    if request.form.get('important') == 'on':
        important = True
    else:
        important = False
    
    userId = flaskSession.get('userId')


    if request.form['group-select'] != 'new':
        groupId = request.form['group-select']
        group = sessionDb.query(Group).filter(Group.group_id == groupId).first()
        
    else:
        new_group_name = request.form['new-group-input']
        if len(new_group_name) < 50 and new_group_name != '': # Group name must be less than 50 characters
            new_group = Group(user_id=userId, group_name=new_group_name, group_id=str(uuid.uuid4()))
            sessionDb.add(new_group)
            sessionDb.commit()
            group = new_group
        else:
            errors.append('group_name_length')


    
    if dueDate == '':
        errors.append('empty_field')
    dueDate = datetime.datetime.strptime(dueDate, '%Y-%m-%d').date()
    
    userId = flaskSession.get('userId')

    # Check for errors in the form data
    if name == '':
        errors.append('empty_field')
    
    if len(errors) > 0:
        groups = sessionDb.query(Group).filter(Group.user_id == flaskSession.get('userId')).all()
        return render_template('edit_task.html', errors=errors,groups=groups)
    else:
        group_id = sessionDb.query(Group).filter(Group.group_name == group.group_name and Group.user_id == userId).first().group_id

        task = sessionDb.query(Task).filter(Task.task_id == task_id).first()
        task.name = name
        task.details = details
        task.group_id = group_id
        task.important = important
        task.due_date = dueDate
        sessionDb.commit()

        flash('Task edited successfully!')
        return redirect(url_for('dashboard'))

#Delete task
@app.route('/deletetask/<task_id>')
def deleteTask(task_id):
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    task = sessionDb.query(Task).filter(Task.task_id == task_id).first()
    if task:
        sessionDb.delete(task)
        sessionDb.commit()

    flash('Task deleted.')
    return redirect(url_for('dashboard'))

#My Day page
@app.route('/myday')
def myday():
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    userId = flaskSession.get('userId')
    
    # Get tasks due today - needs to filter by date separately because the date is stored as a datetime object
    current_date = datetime.datetime.now().date()
    tasks = sessionDb.query(Task).filter(Task.user_id == userId).all()
    tasks = [task for task in tasks if task.due_date.date() == current_date]


    return render_template('myday.html', tasks=tasks, showDetails=True)

#Log out
@app.route('/logout')
def logout():
    flaskSession.clear()
    return redirect(url_for('home'))

# Toggles the hide completed tasks setting for the dashboard
@app.route('/hide_completed', methods=['POST'])
def hideCompleted():
    flaskSession['hideCompleted'] = not flaskSession.get('hideCompleted')
    return redirect(url_for('dashboard'))

#Delete group
@app.route('/deletegroup/<group_id>')
def deleteGroup(group_id):
    if flaskSession.get('userId') is None:
        return redirect(url_for('login'))

    group = sessionDb.query(Group).filter(Group.group_id == group_id).first()
    if group:
        sessionDb.delete(group)
        sessionDb.commit()

    flash('Group deleted.')
    return redirect(url_for('dashboard'))

app.run(debug=True, reloader_type='stat', port=5000)