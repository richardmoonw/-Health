import sqlite3
import os
from flask import Flask, request, render_template, redirect, session
from werkzeug import secure_filename


#Python module to be able to hash the passwords
import hashlib

from Doctors import account_controller, account_manager, doctor_dao
from Diagnosis import diagnosis_controller, diagnosis_manager, diagnosis_dao
from Prescriptions import prescription_controller, prescription_manager, prescription_dao
from Patient import patient_dao, patient_manager, patient_controller
from MedicalStudy import upload_studies_controller, upload_studies_manager, medical_studies_dao
from Controllers import document_controller, code_controller
from Managers import document_manager, code_manager

app = Flask(__name__)
app.secret_key = "O@''bw9QWHjx9|]"

#Configure the types of files that we accept to avoid uploading unnecesary 
#files to the database
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#global variables that allow us to access a certain patient and/or doctor from
#diferent pages
doctor_id = 0
patient_id = 0


@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():

	global doctor_id

	if request.method == "POST":
		#Assign of variables from the form input to create the doctor
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

		#create the doctor controller to assign the variables to create a doctor.
		medic = account_controller.AccountController()
		medic.enter_new_account_information(first_name, last_name, email, password, birthdate, phone, sex,\
							school, graduation_date, speciality, hospital)

		#Run the validation to be able to avoid errors when uploading the doctor to the
		#database
		is_valid = account_manager.AccountManager.validate_information(medic)

		if is_valid:
			#Add the validated doctor to the database for future use
			doc = doctor_dao.DoctorDAO.create_new_doctor(medic)
			doctor_id = doc[0]
			return redirect('/upload_degree')

	return render_template('sign_up.html')

@app.route('/upload_degree', methods=["GET", "POST"])
def upload_degree():
	global doctor_id

	if request.method == "POST":
		#Assign the needed path and configuration to save files
		UPLOAD_FOLDER = './static/medical_degrees/'
		app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

		#Grab the file selected by the doctor and saves them in a specified path
		file = request.files['medical_study']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		#create the document controller to assign the variables to create a degree.
		document_con = document_controller.DocumentController()
		document_con.upload_medical_degree(doctor_id, filename)

		#Run the validation to be able to avoid errors when uploading the doctor to the
		#database
		is_valid = document_manager.DocumentManager.validate_degree(document_con)

		if is_valid == True:
			#Add the validated degree to the database for future use
			doctor_dao.DoctorDAO.create_degree(document_con)
			doctor_id = 0
			return redirect('/')

	return render_template('upload_degree.html')

@app.route('/logout')
def logout():
	#We clear the session to be able to change between diferent users
	session.clear()
	return redirect('/')


@app.route('/login_patient', methods=["GET", "POST"])
def login_patient():

	global patient_id

	is_user = False

	if request.method == 'POST':
		#Assign of variables from the form input to login to a patient account
		email = request.form.get("email")
		password = request.form.get("password")


		user = patient_dao.PatientDAO.validate_login(email)

		#We pass the password to the hash function to compare it with
		#the encrypted one in the database
		encrypted_pwd = hashlib.sha256(password.encode()).hexdigest()

		if encrypted_pwd == user[1]:
			is_user = True

		#We check if the session is active to be able to access the database
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

		#Assign of variables from the form input to login to a doctor account
		email = request.form.get("email")
		password = request.form.get("password")

		user = doctor_dao.DoctorDAO.validate_login(email)

		#We pass the password to the hash function to compare it with
		#the encrypted one in the database
		encrypted_pwd = hashlib.sha256(password.encode()).hexdigest()

		if encrypted_pwd == user[1]:
			is_user = True

		#We check if the session is active to be able to access the database
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

	#we get the doctor of the current session to access its data
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

		#constructs a code to be able to send it to the db to compare it
		pat_code = code_controller.CodeController()
		pat_code.enter_patients_code(patient_id2)

		#Validates the code before using it
		is_valid = code_manager.CodeManager.validate_code(pat_code)

		if is_valid == True:
			#Gets the code of the patient and sends the code
			patient = patient_dao.PatientDAO.get_patient(patient_id2)	

			if patient[9] == doctor_id:
				patient_id = patient_id2
				return redirect('/view_patient')

			#asks for confirmation from the patient so we can access its data
			patient_dao.PatientDAO.request_access(doctor_id, patient_id2)
			patient = patient_dao.PatientDAO.get_patient(patient_id2)	

			return render_template('search_patient.html', patient=patient)


	if 'name' in session:
		return render_template('search_patient.html')
	else:
		return redirect('/')

@app.route('/view_patient', methods=["GET", "POST"])
def view_patient():
	patient = patient_dao.PatientDAO.get_patient(patient_id)
	if request.method == "POST":
		treatments = []

		#Constructs a code to be able to send it to the db to compare it
		pat_code = code_controller.CodeController()
		pat_code.enter_patients_code(patient_id)

		#Validates the code before using it
		is_valid = code_manager.CodeManager.validate_code(pat_code)

		if is_valid == True:

			#Selects each item of the prescription from the database and grabs them
			files = patient_dao.PatientDAO.get_medical_history(pat_code)
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
		#Request general info from the patient
		patient_manager.PatientManager.request_general_information(patient_id)
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

		#Configures the path and the folder that will save the medical study 
		UPLOAD_FOLDER = './static/studies/'
		app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

		#Gets the file that the patient selected and saves it in the specified folder
		file = request.files['medical_study']
		date = request.form.get("date_created")
		description = request.form.get("description")
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
		#creates the study constructor to be able to send it to the database
		study = upload_studies_controller.UploadStudiesController()
		study.upload_new_medical_study()
		study.add_medical_study(patient_id, filename, date, description)

		#validates the info of the created study
		is_valid = upload_studies_manager.UploadStudiesManager.validate_medical_study(study)

		if is_valid == True:

			#Saves the validated study to the database
			medical_studies_dao.MedicalStudiesDAO.create_medical_study(study)

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

		#Gets the information from the form 
		quantity = int(request.form.get("treatment_count"))
		treatment_date = request.form.get("treatment_date")

		description = []
		dose = []
		administration = []
		frequency_value = []
		frequency = []

		#Goes through each invividual prescription item and appends them to a list
		for x in range(1, quantity+1):			
			description.append(request.form.get("description" + str(x)))
			dose.append(request.form.get("dose" + str(x)))
			administration.append(request.form.get("administration" + str(x)))
			frequency_value.append(request.form.get("frequency_value" + str(x)))
			frequency.append(request.form.get("frequency" + str(x)))

		#Creates a new prescription object with the given list
		pres = prescription_controller.PrescriptionController()
		pres.create_new_prescription()
		pres.add_prescription(description, doctor_id, treatment_date, dose, \
								administration, frequency_value, frequency)


		#validates the prescription object
		is_valid = prescription_manager.PrescriptionManager.validate_prescription_information(pres)

		if is_valid == True:
			#Saves the validated prescription object to the database
			prescription_dao.PrescriptionDAO.create_prescription(pres)

	if 'name' in session:
		return render_template('new_treatment.html')
	else:
		return redirect('/')
	

@app.route('/new_diagnosis', methods=["GET", "POST"])
def new_diagnosis():
	if request.method == "POST":

		#Gets the diagnosis information from the form
		date_created = request.form.get("date_created")
		description = request.form.get("description")

		#Create a diagnosis object
		diag = diagnosis_controller.DiagnosisController()
		diag.create_new_diagnosis()
		diag.add_diagnosis(date_created, description, doctor_id)

		#Validate diagnosis
		is_valid = diagnosis_manager.DiagnosisManager.validate_diagnosis_information(diag)

		if is_valid == True:
			#access the database
			diagnosis_dao.DiagnosisDAO.create_diagnosis(diag)


	if 'name' in session:
		return render_template('new_diagnosis.html')
	else:
		return redirect('/')


@app.route('/medical_history')
def medical_history():
	# before patient = patient_dao.PatientDAO.get_patient(patient_id)
	patient_con = patient_controller.PatientController()
	patient = patient_con.request_medical_history(patient_id)

	if 'name' in session:
		return render_template('medical_history.html', patient = patient)
	else:
		return redirect('/')
	

