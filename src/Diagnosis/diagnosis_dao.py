from DatabaseConnection import connection

class DiagnosisDAO:
    def add_diagnosis(diagnosis):
        conn = connection.Connection.make_connection()

        cur = conn.cursor()

        cur.execute("SELECT id FROM Doctor WHERE name='" + diagnosis.doctor_id + "'") 
        doctor_id = cur.fetchone()

        cur.execute("INSERT INTO Diagnosis (date_created, description, doctor_id) VALUES(?,?,?)", \
                    (diagnosis.date_created, diagnosis.description, diagnosis.doctor_id[0]))

        conn.commit()

        conn.close()

    def get_doctor_id(id):
        conn = connection.Connection.make_connection()

        cur = conn.cursor()

        cur.execute("SELECT doctor_id FROM Diagnosis WHERE Diagnosis.doctor_id=" + str(id))

        doctor_id = cur.fetchone()

        return doctor_id

    # def get_file_id(id):
	# 	conn = connection.Connection.make_connection()

	# 	cur = conn.cursor()

	# 	cur.execute("SELECT file_id FROM Diagnosis WHERE file_id ='" + file_id + "'")

	# 	file_id = cur.fetchone()

	# 	return file_id """