from flask import Flask, render_template

app = Flask(__name__)

#Welcome page when not signed in
@app.route('/')
def home():
    return render_template('index.html')


#Login/signup pages

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')


#Main page after login
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

app.run(debug=True, reloader_type='stat', port=5000)