from DatabaseConnection import connection

class PrescriptionDAO:
    def create_prescription(treatment):
        conn = connection.Connection.make_connection()

        cur = conn.cursor()

        # Obtener el id del historial
        cur.execute("SELECT id FROM MedicalHistory WHERE patient_id=" + str(treatment.patient_id))
        history_id = cur.fetchone()

        # Hacer el medical file
        cur.execute("INSERT INTO MedicalFile (date, type, history_id) VALUES (?, ?, ?)", (treatment.date_created, \
                    treatment._type, history_id[0]))
        conn.commit()

        cur.execute("SELECT MAX(id) FROM MedicalFile")
        file_id = cur.fetchone()

        # Hacer el treatment
        cur.execute("INSERT INTO Treatment (doctor_id, file_id) VALUES(?,?)", \
                    (treatment.doctor_id, file_id[0]))
        conn.commit()

        cur.execute("SELECT MAX(id) FROM Treatment")
        treatment_id = cur.fetchone()

        for x in range(0, len(treatment.description)):
            cur.execute("SELECT id FROM TreatmentItem WHERE name='" + treatment.description[x] + "'")
            item_id = cur.fetchone()

            cur.execute("INSERT INTO TreatmentList(item_id, treatment_id, frequency, dose, administration) VALUES (?, ?, ?, ?, ?)", (item_id[0], \
                        treatment_id[0], treatment.frequency_value[x] + " " + treatment.frequency[x], treatment.dose[x], treatment.administration[x]))
            conn.commit()

        conn.close()