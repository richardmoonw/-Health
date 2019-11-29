from DatabaseConnection import connection 

class PatientDAO:
	def get_medical_history(patient):
		files = []

		conn = connection.Connection.make_connection()

		cur = conn.cursor()

		cur.execute("SELECT id FROM MedicalHistory WHERE patient_id=" + str(patient.patient_id))
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

		conn.close() 

		return files

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

	def get_drugs():
		conn = connection.Connection.make_connection()

		cur = conn.cursor()

		cur.execute("SELECT * FROM TreatmentItem")
		drugs = cur.fetchall()

		conn.close()

		return drugs





