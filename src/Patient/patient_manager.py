from Patient import patient_dao

class PatientManager:

	def request_general_information(patient_code):
		patient_dao.PatientDAO.retrieve_general_information(patient_code)

	def retrieve_medical_history(patient_code):
		medical_history = patient_dao.PatientDAO.get_patient

		return medical_history

	#Now in code manager
	# def validate_information(patient):

	# 	is_valid = True

	# 	if patient._id is None:
	# 		is_valid = False

	# 	return is_valid