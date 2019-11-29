import sqlite3
import os
from flask import Flask, request, render_template, redirect, session
from werkzeug import secure_filename

import hashlib

from Doctors import doctor, doctor_controller, doctor_dao
from Diagnosis import diagnosis, diagnosis_controller, diagnosis_dao
from Prescriptions import prescription, prescription_manager, prescription_dao
from Patient import patient_controller, patient_manager, patient_dao

app = Flask(__name__)
app.secret_key = "O@''bw9QWHjx9|]"
UPLOAD_FOLDER = './static/medical_degrees/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/upload_degree', methods=["GET", "POST"])
def upload_degree():

	if request.method == "POST":
		file = request.files['medical_study']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print("All right")

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

@app.route('/view_patient', methods=["GET", "POST"])
def view_patient():
	if request.method == "POST":
		treatments = []
		pat = patient_controller.PatientController()

		is_valid = patient_manager.PatientManager.validate_information(pat)

		if is_valid == True:
			files = patient_dao.PatientDAO.get_medical_history(pat)
			for file in files:
				if file[0] == "treatment":
					treatments.append(patient_dao.PatientDAO.get_list(file[4]))
			drugs = patient_dao.PatientDAO.get_drugs()

			print(treatments)

			return render_template('medical_history.html', medical_files=files, treatments=treatments, drugs=drugs)


	return render_template('view_patient.html')

@app.route('/patient_profile')
def patient_profile():
	return render_template('patient_profile.html')

@app.route('/upload_study')
def upload_study():
	return render_template('upload_study.html')

@app.route('/new_treatment', methods=["GET", "POST"])
def new_treatment():
	if request.method == "POST":
		quantity = int(request.form.get("treatment_count"))
		treatment_date = request.form.get("treatment_date")

		description = []
		dose = []
		administration = []
		frequency_value = []
		frequency = []

		for x in range(1, quantity+1):			
			description.append(request.form.get("description" + str(x)))
			dose.append(request.form.get("dose" + str(x)))
			administration.append(request.form.get("administration" + str(x)))
			frequency_value.append(request.form.get("frequency_value" + str(x)))
			frequency.append(request.form.get("frequency" + str(x)))

		pres = prescription.PrescriptionController(description, 1, treatment_date, dose, \
													administration, frequency_value, frequency)

		is_valid = prescription_manager.PrescriptionManager.validate_data(pres)

		if is_valid == True:
			prescription_dao.PrescriptionDAO.add_treatment(pres)

	return render_template('new_treatment.html')

@app.route('/new_diagnosis', methods=["GET", "POST"])
def new_diagnosis():
	if request.method == "POST":
		date_created = request.form.get("date_created")
		description = request.form.get("description")

		diag = diagnosis.Diagnosis(date_created, description, 1)

		is_valid = diagnosis_controller.DiagnosisController.validate_data(diag)

		if is_valid == True:
			diagnosis_dao.DiagnosisDAO.add_diagnosis(diag)

	return render_template('new_diagnosis.html')


@app.route('/medical_history')
def medical_history():
	return render_template('medical_history.html')

