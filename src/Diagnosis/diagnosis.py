class Diagnosis:
	def __init__(self, date_created, description, file_id, doctor_id):
		self.date_created = date_created
		self.description = description
		self.file_id = file_id
		self.doctor_id = doctor_id

		self.type = "diagnosis"