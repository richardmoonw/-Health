import sqlite3
from flask import Flask, request, render_template, redirect, session

import hashlib

from Doctors import doctor, doctor_controller, doctor_dao
from Diagnosis import diagnosis, diagnosis_controller, diagnosis_dao

app = Flask(__name__)
app.secret_key = "O@''bw9QWHjx9|]"

doctor_id = 0

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
	if request.method == "POST":
		first_name = request.form.get("first_name")
		last_name = request.form.get("last_name")
		email = request.form.get("email")
		password = request.form.get("password")
		birthdate = request.form.get("birthdate")
		phone = request.form.get("phone")
		sex = request.form.get("sex")
		school = request.form.get("school")
		graduation_date = request.form.get("graduation")
		speciality = request.form.get("speciality")
		hospital = request.form.get("hospital")

		medic = doctor.Doctor(first_name, last_name, email, password, birthdate, phone, sex,\
							school, graduation_date, speciality, hospital)

		is_valid = doctor_controller.DoctorController.validate_data(medic)

		if is_valid == True:
			doctor_dao.DoctorDAO.add_doctor(medic)

	return render_template('sign_up.html')

@app.route('/upload_degree')
def upload_degree():
	return render_template('upload_degree.html')

@app.route('/login', methods=["GET", "POST"])
def login():
	is_user = False

	if request.method == 'POST':

		# Employee Data
		email = request.form.get("email")
		password = request.form.get("password")

		user = doctor_dao.DoctorDAO.validate_login(email)

		encrypted_pwd = hashlib.sha256(password.encode()).hexdigest()

		if encrypted_pwd == user[1]:
			is_user = True

		if is_user:
			session['name'] = user
			doctor_id = session['name'][0]

			doctor = doctor_dao.DoctorDAO.get_doctor(doctor_id)

			return render_template("doctor_profile.html", first_name = doctor[1], last_name = doctor[2], \
							hospital = doctor[14], phone = doctor[5], email = doctor[8], \
							street = doctor[15], zip_code = doctor[16], city = doctor[17], state = doctor[18], \
							birthdate = doctor[3], sex = doctor[4], speciality = doctor[7], school = doctor[21], \
							graduation_date = doctor[12])

		else:
			return redirect("/login")

	return render_template("login.html")

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

@app.route('/upload_study')
def upload_study():
	return render_template('upload_study.html')

@app.route('/new_treatment')
def new_treatment():
	return render_template('new_treatment.html')

@app.route('/new_diagnosis', methods=["GET", "POST"])
def new_diagnosis():
	if request.method == "POST":
		date_created = request.form.get("date_created")
		description = request.form.get("description")

		diagnosis = diagnosis.Diagnosis(date_created, description)

		#doctor_id = diagnosis_dao.DiagnosisDAO.get_doctor_id(doctor_id)

		is_valid = diagnosis_controller.DiagnosisController.validate_data(diagnosis)

		if is_valid == True:
			diagnosis_dao.DiagnosisDAO.add_diagnosis(diagnosis)

	return render_template('new_diagnosis.html')


@app.route('/medical_history')
def medical_history():
	return render_template('medical_history.html')