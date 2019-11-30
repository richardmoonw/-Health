from DatabaseConnection import connection 

#Class in charge of accessing the database and updating the information
#related to the patient
class PatientDAO:

	#Select a patient and returns
	def get_medical_history(patient):
		files = []

		conn = connection.Connection.make_connection()

		cur = conn.cursor()

		cur.execute("SELECT id FROM MedicalHistory WHERE patient_id=" + str(patient._id))
		history_id = cur.fetchone()

		cur.execute("SELECT * FROM MedicalFile WHERE history_id=" + str(history_id[0]) + " ORDER BY date DESC")
		medical_files = cur.fetchall()

		for file in medical_files:
			if file[2] == "diagnosis":
				cur.execute("SELECT MedicalFile.type, MedicalFile.date, Doctor.first_name, Doctor.last_name, Diagnosis.description \
							FROM Diagnosis JOIN Doctor ON Diagnosis.doctor_id = Doctor.id \
							JOIN MedicalFile ON Diagnosis.file_id = MedicalFile.id \
							WHERE file_id=" + str(file[0]))
				diagnosiss = cur.fetchall()

				for diagnosis in diagnosiss:
					files.append(diagnosis)


			elif file[2] == "treatment":
				cur.execute("SELECT MedicalFile.type, MedicalFile.date, Doctor.first_name, Doctor.last_name , Treatment.id, \
							Treatment.file_id \
							FROM Treatment JOIN Doctor ON Treatment.doctor_id = Doctor.id \
							JOIN MedicalFile ON Treatment.file_id = MedicalFile.id \
							WHERE file_id=" + str(file[0]))
				treatments = cur.fetchall()

				for treatment in treatments:
					files.append(treatment)

			elif file[2] == "study":
				cur.execute("SELECT MedicalFile.type, MedicalFile.date, MedicalStudy.description, MedicalStudy.file \
							FROM MedicalStudy JOIN MedicalFile ON MedicalStudy.file_id = MedicalFile.id \
							WHERE file_id=" + str(file[0]))
				studies = cur.fetchall()

				for study in studies:
					files.append(study)

		conn.close() 

		return files

	#Get the prescription items and returns them
	def get_list(treatment_id):
		treatments = []

		conn = connection.Connection.make_connection()

		cur = conn.cursor()

		cur.execute("SELECT * FROM TreatmentList WHERE treatment_id=" + str(treatment_id))
		treatment_list = cur.fetchall()

		if treatment_list is not None:
			for treatment in treatment_list:
				treatments.append(treatment)

		conn.close()

		return treatments

	#Select the drugs that are in the database
	def get_drugs():
		conn = connection.Connection.make_connection()

		cur = conn.cursor()

		cur.execute("SELECT * FROM TreatmentItem")
		drugs = cur.fetchall()

		conn.close()

		return drugs

	#Selects the encrypted password and return it
	def validate_login(email):
		conn = connection.Connection.make_connection()

		cur = conn.cursor()

		cur.execute("SELECT id, password FROM Patient WHERE email ='" + email + "'")
		user = cur.fetchone()

		conn.close()

		return user

	#Get all the atributes of a specific patient
	def get_patient(id):
		conn = connection.Connection.make_connection()

		cur = conn.cursor()

		cur.execute("SELECT * FROM Patient WHERE id=" + str(id))
		patient = cur.fetchone()

		conn.close()

		return patient

	#Updating the flags needed to give access
	def request_access(doctor_id, patient_id):
		conn = connection.Connection.make_connection()

		cur = conn.cursor()
		cur.execute("UPDATE Patient SET access_flag=1, doctor_access = " +str(doctor_id) + " WHERE id = " + str(patient_id))
		conn.commit()

		conn.close()

	#Updating the flags after being given access by the patient
	def retrieve_general_information(patient_id):
		conn = connection.Connection.make_connection()

		cur = conn.cursor()
		cur.execute("UPDATE Patient SET access_flag=0 WHERE id = " + str(patient_id))
		conn.commit()

		conn.close()



