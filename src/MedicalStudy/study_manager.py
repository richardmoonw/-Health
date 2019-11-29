class StudyManager:
	def validate_information(patient):

		is_valid = True

		if patient.patient_id is None:
			is_valid = False

		elif patient.date is None:
			is_valid = False

		if patient.type is None:
			is_valid = False

		if patient.description is None:
			is_valid = False

		return is_valid