#Class in charge of validating the diagnosis
class DiagnosisManager:
	def validate_diagnosis_information(diagnosis):
		is_valid = True

		if diagnosis.patient_id is None:
			is_valid = False

		if diagnosis._type is None:
			is_valid = False

		if diagnosis.date_created is None:
			is_valid = False
        
		elif diagnosis.description is None:
			is_valid = False

		elif diagnosis.doctor_id is None:
			is_valid = False

		return is_valid
