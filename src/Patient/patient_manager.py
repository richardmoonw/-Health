class PatientManager:
	def validate_information(patient):

		is_valid = True

		if patient.patient_id is None:
			is_valid = False

		return is_valid