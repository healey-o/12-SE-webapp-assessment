from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = '0f71536e0640da386f0537f1'

engine = create_engine('sqlite:///userdata.db')
connection = engine.connect()

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
    
    query = text("SELECT * FROM userdetails WHERE username = '{}'".format(username))
    result = connection.execute(query).fetchall()
    if len(result) > 0:
        errors.append('username_taken')

    

    if len(errors) > 0:
        return render_template('signup.html', errors=errors)
    else:
        unique_id = str(uuid.uuid4())#gives each user a unique id
        insert_statement = '''
    INSERT INTO userdetails (id, username, password)
    VALUES ('{}', '{}', '{}');
    '''.format(unique_id, username, password, unique_id, unique_id)
    
        connection.execute(text(insert_statement))
        connection.commit()

        insert_statement = '''
    INSERT INTO groups (user_id, group_name)
    VALUES 
    ('{}', 'Personal'),
    ('{}', 'School');
    '''.format(unique_id, unique_id)
        
        connection.execute(text(insert_statement))
        connection.commit()

        

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
    query = text("SELECT * FROM userdetails WHERE username = '{}' and password = '{}'".format(username, password))
    result = connection.execute(query).fetchall()
    if len(result) == 0:
        return render_template("login.html",failed_attempt=True)
    else:
        # Set the session variables
        session['userId'] = result[0][0]
        session['username'] = result[0][1]
        return redirect(url_for('dashboard'))
    


#Main page after login
@app.route('/dashboard')
def dashboard():
    userId = session.get('userId')
    if userId is None:
        return redirect(url_for('login'))
    else:
        query = text("SELECT * FROM tasks WHERE user_id = '{}'".format(userId))
        result = connection.execute(query).fetchall()

        print(userId)
        groups_query = text("SELECT group_name FROM groups WHERE user_id = '{}'".format(userId))
        groups = [group[0] for group in connection.execute(groups_query).fetchall()]
        print(groups)

        for task in result:
            if task[4] not in groups:
                groups.append(task[4])

        return render_template('dashboard.html', tasks=result, groups=groups)

@app.route('/complete', methods=['POST'])
def completeTask():
    task_id = request.form['task_id']
    query = text("UPDATE tasks SET completed = 1 WHERE task_id = '{}'".format(task_id))
    connection.execute(query)
    return redirect(url_for('dashboard'))

@app.route('/addtask', methods=['GET'])
def addtask():
    groups_query = text("SELECT group_name FROM groups WHERE user_id = '{}'".format(session.get('userId')))
    groups = [group[0] for group in connection.execute(groups_query).fetchall()]

    return render_template('add_task.html',groups=groups)

@app.route('/addtask', methods=['POST'])
def submitTask():
    errors = []

    # Get the form data
    task = request.form['task']

    if request.form['group-select'] != 'new':
        print(request.form.get('group-select'))
        group = request.form['group-select']
    else:
        group = request.form['new-group-input']

    details = request.form['description']

    due_date = request.form['due-date']
    if due_date == '':
        errors.append('empty_field')

    if request.form.get('important') == 'on':
        important = 1
    else:
        important = 0
    
    userId = session.get('userId')

    groups_query = text("SELECT group_name FROM groups WHERE user_id = '{}'".format(userId))
    groups = [group[0] for group in connection.execute(groups_query).fetchall()]

    if group not in groups:
        insert_statement = '''
    INSERT INTO groups (user_id, group_name)
    VALUES ('{}', '{}')
    '''.format(userId, group)
        connection.execute(text(insert_statement))
        connection.commit()

    # Check for errors in the form data
    if task == '':
        errors.append('empty_field')
    
    if len(errors) > 0:
        return render_template('add_task.html', errors=errors,groups=groups)
    else:
        insert_statement = '''
    INSERT INTO tasks (user_id, task_id, name, details, group_name, important, due_date, completed)
    VALUES ('{}', '{}', '{}', '{}', '{}', {}, '{}', 0)
    '''.format(userId, str(uuid.uuid4()), task, details, group, important, due_date)

        connection.execute(text(insert_statement))
        connection.commit()

        return redirect(url_for('dashboard'))

app.run(debug=True, reloader_type='stat', port=5000)