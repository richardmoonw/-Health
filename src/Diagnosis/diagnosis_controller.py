class DiagnosisController:
	def validate_data(diagnosis):
        is_valid = True

        if diagnosis.date is None:
			is_valid = False
        
		elif diagnosis.description is None:
			is_valid = False

		elif diagnosis.file_id is None:
			is_valid = False

		elif diagnosis.doctor_id is None:
			is_valid = False

        return is_valid
