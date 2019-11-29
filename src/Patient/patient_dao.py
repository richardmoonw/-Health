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
				cur.execute("SELECT MedicalFile.date, Diagnosis.description, Doctor.first_name, Doctor.last_name \
							FROM Diagnosis JOIN Doctor ON Diagnosis.doctor_id = Doctor.id \
							JOIN MedicalFile ON Diagnosis.file_id = MedicalFile.id \
							WHERE file_id=" + str(file[0]))
				diagnosiss = cur.fetchall()

				for diagnosis in diagnosiss:
					files.append(diagnosiss)


			elif file[2] == "treatment":
				cur.execute("SELECT MedicalFile.date, Treatment.id, Treatment.file_id, Doctor.first_name, Doctor.last_name \
							FROM Treatment JOIN Doctor ON Treatment.doctor_id = Doctor.id \
							JOIN MedicalFile ON Treatment.file_id = MedicalFile.id \
							WHERE file_id=" + str(file[0]))
				treatments = cur.fetchall()

				for treatment in treatments:
					drugs = []

					

		print(files)

		conn.close() 