#Class in charge of creating the diagnosis object
class DiagnosisController:
	patient_id = 1
	_type = "diagnosis"
	date_created = ""
	description = ""
	doctor_id = 0

	#Instantiate the variables
	def create_new_diagnosis(self):
		self.patient_id = 1
		self._type = "diagnosis"
		self.date_created = ""
		self.description = "description"
		self.doctor_id = 0

	#Update the variables with the doctors input
	def add_diagnosis(self, date_created, description, doctor_id):
		self.patient_id = 1
		self._type = "diagnosis"
		self.date_created = date_created
		self.description = description
		self.doctor_id = doctor_id