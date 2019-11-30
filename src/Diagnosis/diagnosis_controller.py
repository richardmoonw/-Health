#before Diagnosis
class DiagnosisController:
	patient_id = 1
	_type = "diagnosis"
	date_created = ""
	description = ""
	doctor_id = 0

	def create_new_diagnosis(self):
		self.patient_id = 1
		self._type = "diagnosis"
		self.date_created = ""
		self.description = "description"
		self.doctor_id = 0

	def add_diagnosis(self, date_created, description, doctor_id):
		self.patient_id = 1
		self._type = "diagnosis"
		self.date_created = date_created
		self.description = description
		self.doctor_id = doctor_id