class Diagnosis:
	def __init__(self, date_created, description, doctor_id):
		self.date_created = date_created
		self.description = description
		self.doctor_id = doctor_id

		self.type = "diagnosis"