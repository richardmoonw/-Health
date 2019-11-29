import sqlite3
import os
from flask import Flask, request, render_template, redirect, session
from werkzeug import secure_filename

import hashlib

from Doctors import doctor, doctor_controller, doctor_dao
from Diagnosis import diagnosis, diagnosis_controller, diagnosis_dao
from Prescriptions import prescription, prescription_manager, prescription_dao
from Patient import patient_controller, patient_manager, patient_dao
from MedicalStudy import study_controller, study_manager, study_dao

app = Flask(__name__)
app.secret_key = "O@''bw9QWHjx9|]"
# UPLOAD_FOLDER = './static/medical_degrees/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

doctor_id = 0
patient_id = 0

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():

	global doctor_id

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

		medic = doctor.Doctor()
		medic.create_doctor(first_name, last_name, email, password, birthdate, phone, sex,\
							school, graduation_date, speciality, hospital)

		is_valid = doctor_controller.DoctorController.validate_data(medic)

		if is_valid == True:
			doc = doctor_dao.DoctorDAO.add_doctor(medic)
			doctor_id = doc[0]
			return redirect('/upload_degree')

	return render_template('sign_up.html')

@app.route('/upload_degree', methods=["GET", "POST"])
def upload_degree():
	global doctor_id

	if request.method == "POST":
		UPLOAD_FOLDER = './static/medical_degrees/'
		app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
		file = request.files['medical_study']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		medic = doctor.Doctor()
		medic.create_degree(doctor_id, filename)

		is_valid = doctor_controller.DoctorController.validate_doctor(medic)

		if is_valid == True:
			doc = doctor_dao.DoctorDAO.new_degree(medic)
			doctor_id = 0
			return redirect('/')

	return render_template('upload_degree.html')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')


@app.route('/login_patient', methods=["GET", "POST"])
def login_patient():

	global patient_id

	is_user = False

	if request.method == 'POST':

		email = request.form.get("email")
		password = request.form.get("password")

		user = patient_dao.PatientDAO.validate_login(email)

		encrypted_pwd = hashlib.sha256(password.encode()).hexdigest()

		if encrypted_pwd == user[1]:
			is_user = True

		if is_user:
			session['name'] = user
			patient_id = session['name'][0]

			patient = patient_dao.PatientDAO.get_patient(patient_id)

			return redirect("/patient_profile")

		else:
			return redirect("/login_patient")

	return render_template("login_patient.html")


@app.route('/login', methods=["GET", "POST"])
def login():

	global doctor_id 

	is_user = False

	if request.method == 'POST':

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

			return redirect("/doctor_profile")

		else:
			return redirect("/login")

	return render_template("login.html")


@app.route('/doctor_profile')
def doctor_profile():
	doctor = doctor_dao.DoctorDAO.get_doctor(doctor_id)

	if 'name' in session:

		return render_template("doctor_profile.html", first_name = doctor[1], last_name = doctor[2], \
							hospital = doctor[14], phone = doctor[5], email = doctor[8], \
							street = doctor[15], zip_code = doctor[16], city = doctor[17], state = doctor[18], \
							birthdate = doctor[3], sex = doctor[4], speciality = doctor[7], school = doctor[21], \
							graduation_date = doctor[12])
	else:
		return redirect('/')


@app.route('/search_patient', methods=["GET", "POST"])
def search_patient():
	global patient_id

	if request.method == "POST":
		patient_id2 = request.form.get("patient_id")

		pat = patient_controller.PatientController(patient_id2)

		is_valid = patient_manager.PatientManager.validate_information(pat)

		if is_valid == True:
			patient = patient_dao.PatientDAO.get_patient(patient_id2)	

			if patient[9] == doctor_id:
				patient_id = patient_id2
				return redirect('/view_patient')

			patient_dao.PatientDAO.request_access(doctor_id, patient_id2)
			patient = patient_dao.PatientDAO.get_patient(patient_id2)	

			return render_template('search_patient.html', patient=patient)


	if 'name' in session:
		return render_template('search_patient.html')
	else:
		return redirect('/')

# FOCO ROJO
@app.route('/view_patient', methods=["GET", "POST"])
def view_patient():
	patient = patient_dao.PatientDAO.get_patient(patient_id)
	if request.method == "POST":
		treatments = []
		pat = patient_controller.PatientController(patient_id)

		is_valid = patient_manager.PatientManager.validate_information(pat)

		if is_valid == True:
			files = patient_dao.PatientDAO.get_medical_history(pat)
			for file in files:
				if file[0] == "treatment":
					treatments.append(patient_dao.PatientDAO.get_list(file[4]))
			drugs = patient_dao.PatientDAO.get_drugs()

			print(files)

			return render_template('medical_history.html', medical_files=files, treatments=treatments, drugs=drugs, patient=patient)

	if 'name' in session:
		return render_template('view_patient.html', patient=patient)
	else:
		return redirect('/')


@app.route('/patient_profile', methods=["GET", "POST"])
def patient_profile():
	patient = patient_dao.PatientDAO.get_patient(patient_id)
	doc = doctor_dao.DoctorDAO.get_doctor(patient[9])

	if request.method == "POST":
		patient_dao.PatientDAO.allow_access(patient_id) 
		return redirect('/patient_profile')

	if 'name' in session:
		return render_template("patient_profile.html", id = patient[0], first_name = patient[1], last_name = patient[2], \
								email = patient[3], birthdate = patient[5], sex = patient[6], phone = patient[7], \
								flag = patient[8], doctor_access = patient[9], doc_first_name = doc[1], doc_last_name = doc[2], \
								doc_speciality = doc[7])
	else:
		return redirect('/')


@app.route('/upload_study', methods=["GET", "POST"])
def upload_study():
	if request.method == "POST":
		UPLOAD_FOLDER = './static/studies/'
		app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
		file = request.files['medical_study']
		date = request.form.get("date_created")
		description = request.form.get("description")
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
		study = study_controller.StudyController(patient_id, filename, date, description);

		is_valid = study_manager.StudyManager.validate_information(study)

		if is_valid == True:
			study_dao.StudyDAO.add_study(study)

			patient = patient_dao.PatientDAO.get_patient(patient_id)

			return render_template("patient_profile.html", id = patient[0], first_name = patient[1], last_name = patient[2], \
							email = patient[3], birthdate = patient[5], sex = patient[6], phone = patient[7])

	if 'name' in session:
		return render_template('upload_study.html')
	else:
		return redirect('/')
	

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

	if 'name' in session:
		return render_template('new_treatment.html')
	else:
		return redirect('/')
	

@app.route('/new_diagnosis', methods=["GET", "POST"])
def new_diagnosis():
	if request.method == "POST":
		date_created = request.form.get("date_created")
		description = request.form.get("description")

		diag = diagnosis.Diagnosis(date_created, description, 1)

		is_valid = diagnosis_controller.DiagnosisController.validate_data(diag)

		if is_valid == True:
			diagnosis_dao.DiagnosisDAO.add_diagnosis(diag)


	if 'name' in session:
		return render_template('new_diagnosis.html')
	else:
		return redirect('/')


@app.route('/medical_history')
def medical_history():
	patient = patient_dao.PatientDAO.get_patient(patient_id)
	if 'name' in session:
		return render_template('medical_history.html', patient = patient)
	else:
		return redirect('/')
	

