from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/signup')
def sign_up():
	return render_template('sign_up.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/doctor_profile')
def doctor_profile():
	return render_template('doctor_profile.html')

@app.route('/search_patient')
def search_patient():
	return render_template('search_patient.html')