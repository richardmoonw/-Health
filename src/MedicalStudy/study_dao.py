from DatabaseConnection import connection

class StudyDAO:
	def add_study(study):
		conn = connection.Connection.make_connection()

		cur = conn.cursor()

		cur.execute("SELECT id FROM MedicalHistory WHERE patient_id=" + str(study.patient_id))
		history_id = cur.fetchone()

		cur.execute("INSERT INTO MedicalFile (date, type, history_id) VALUES (?, ?, ?)", (study.date, study.type, \
					history_id[0]))
		conn.commit()

		cur.execute("SELECT MAX(id) FROM MedicalFile")
		file_id = cur.fetchone()

		cur.execute("INSERT INTO MedicalStudy (description, file, file_id) VALUES(?, ?, ?)", (study.description, \
					study.name, file_id[0]))
		conn.commit()

		conn.close()