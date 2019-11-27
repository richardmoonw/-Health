from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/sign_up')
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

@app.route('/view_patient')
def view_patient():
	return render_template('view_patient.html')

@app.route('/patient_profile')
def patient_profile():
	return render_template('patient_profile.html')

@app.route('/new_treatment')
def new_treatment():
	return render_template('new_treatment.html')

@app.route('/new_diagnosis')
def new_diagnosis():
	return render_template('new_diagnosis.html')

@app.route('/medical_history')
def medical_history():
	return render_template('medical_history.html')