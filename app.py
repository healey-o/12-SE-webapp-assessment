from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
import uuid
from datetime import datetime

app = Flask(__name__)

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
    VALUES ('{}', '{}', '{}')
    '''.format(unique_id, username, password)
    
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
        return redirect(url_for('dashboard'))
    


#Main page after login
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/addtask', methods=['GET'])
def addtask():
    return render_template('add_task.html',groups=["None","Important","Personal"])#Temporary groups for testing

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

    due_date_str = request.form['due-date']
    if due_date_str == '':
        errors.append('empty_field')
    else:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')

    if request.form.get('important') == 'on':
        important = 1
    else:
        important = 0
    
    userId = '1'#Temporary user id for testing


    # Check for errors in the form data
    if task == '':
        errors.append('empty_field')
    
    if len(errors) > 0:
        return render_template('add_task.html', errors=errors,groups=["None","Important","Personal"])
    else:
        insert_statement = '''
INSERT INTO tasks (user_id, name, details, group_name, important, due_date, completed)
VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
'''.format(userId, task, details, group, important, due_date, 0)

        connection.execute(text(insert_statement))
        connection.commit()

        return redirect(url_for('dashboard'))

app.run(debug=True, reloader_type='stat', port=5000)