from Patient import patient_manager

#Now CodeController
class PatientController:
	patient_code = 0
	def request_medical_history(self, patient_code):
		self.patient_code = patient_code

		medical_history = patient_manager.PatientManager.retrieve_medical_history(self.patient_code)

		return medical_history
