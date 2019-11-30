from Patient import patient_dao

#Calls the methods that update the database
class PatientManager:

	def request_general_information(patient_code):
		patient_dao.PatientDAO.retrieve_general_information(patient_code)

	def retrieve_medical_history(patient_code):
		medical_history = patient_dao.PatientDAO.get_patient

		return medical_history