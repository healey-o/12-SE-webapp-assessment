from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text

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
    
    query = text("SELECT * FROM userlogin WHERE username = '{}'".format(username))
    result = connection.execute(query).fetchall()
    if len(result) > 0:
        errors.append('username_taken')

    

    if len(errors) > 0:
        return render_template('signup.html', errors=errors)
    else:
        insert_statement = '''
INSERT INTO userlogin (username, password)
VALUES ('{}','{}')
'''.format(username,password)
    
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
    query = text("SELECT * FROM userlogin WHERE username = '{}' and password = '{}'".format(username, password))
    result = connection.execute(query).fetchall()
    print(result)
    if len(result) == 0:
        return render_template("login.html",failed_attempt=True)
    else:
        return redirect(url_for('dashboard'))
    


#Main page after login
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


app.run(debug=True, reloader_type='stat', port=5000)