from DatabaseConnection import connection

class DiagnosisDAO:
    def add_diagnosis(diagnosis):
        conn = connection.Connection.make_connection()

        cur = conn.cursor()

        print("Si entro")

        # Obtener el id del historial
        cur.execute("SELECT id FROM MedicalHistory WHERE patient_id=" + str(diagnosis.patient_id))
        history_id = cur.fetchone()

        # Hacer el medical file
        cur.execute("INSERT INTO MedicalFile (date, type, history_id) VALUES (?, ?, ?)", (diagnosis.date_created, \
                    diagnosis.type, history_id[0]))
        conn.commit()

        cur.execute("SELECT MAX(id) FROM MedicalFile")
        file_id = cur.fetchone()

        # Hacer el diagnosis
        cur.execute("INSERT INTO Diagnosis (description, doctor_id, file_id) VALUES(?,?,?)", \
                    (diagnosis.description, diagnosis.doctor_id, file_id[0]))
        conn.commit()

        conn.close()

    # def get_file_id(id):
	# 	conn = connection.Connection.make_connection()

	# 	cur = conn.cursor()

	# 	cur.execute("SELECT file_id FROM Diagnosis WHERE file_id ='" + file_id + "'")

	# 	file_id = cur.fetchone()

	# 	return file_id """