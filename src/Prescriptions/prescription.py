class PrescriptionController:
	def __init__(self, description, doctor_id, date_created, dose, \
				administration, frequency_value, frequency):
		self.description = description
		self.patient_id = 1
		self.doctor_id = doctor_id
		self.type = "treatment"
		self.date_created = date_created
		self.dose = dose
		self.administration = administration
		self.frequency_value = frequency_value
		self.frequency = frequency