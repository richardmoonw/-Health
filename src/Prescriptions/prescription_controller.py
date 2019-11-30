class PrescriptionController:
	description = ""
	patient_id = 0
	doctor_id = 0
	_type = ""
	date_created = "date_created"
	dose = ""
	administration = ""
	frequency_value = ""
	frequency = ""

	def create_new_prescription(self):
		self.description = "description"
		self.patient_id = 0
		self.doctor_id = 0
		self._type = "treatment"
		self.date_created = ""
		self.dose = "dose"
		self.administration = "administration"
		self.frequency_value = "frequency_value"
		self.frequency = "frequency"

	def add_prescription(self, description, doctor_id, date_created, dose, \
				administration, frequency_value, frequency):
		self.description = description
		self.patient_id = 1
		self.doctor_id = doctor_id
		self._type = "treatment"
		self.date_created = date_created
		self.dose = dose
		self.administration = administration
		self.frequency_value = frequency_value
		self.frequency = frequency