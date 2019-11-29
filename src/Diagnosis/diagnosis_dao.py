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