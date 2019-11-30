#Class in charge of validating the study the doctor uploads
class UploadStudiesManager:
	def validate_medical_study(patient):

		is_valid = True

		if patient.patient_id is None:
			is_valid = False

		elif patient.date is None:
			is_valid = False

		if patient._type is None:
			is_valid = False

		if patient.description is None:
			is_valid = False

		return is_valid