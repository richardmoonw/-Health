class DiagnosisController:
	def validate_data(diagnosis):
		is_valid = True

		if diagnosis.patient_id is None:
			is_valid = False

		if diagnosis.type is None:
			is_valid = False

		if diagnosis.date_created is None:
			is_valid = False
        
		elif diagnosis.description is None:
			is_valid = False

		elif diagnosis.doctor_id is None:
			is_valid = False

		return is_valid
