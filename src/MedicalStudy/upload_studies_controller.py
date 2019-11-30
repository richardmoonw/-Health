class UploadStudiesController:

	patient_id = 0
	name = ""
	date = ""
	_type = ""
	description = ""

	def upload_new_medical_study(self):
		self.patient_id = 0
		self.name = "name"
		self.date = "date"
		self._type = "study"
		self.description = "description"

	def add_medical_study(self, patient_id, name, date, description):
		self.patient_id = patient_id
		self.name = name
		self.date = date
		self._type = "study"
		self.description = description

