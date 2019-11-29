class StudyController:
	def __init__(self, patient_id, name, date, description):
		self.patient_id = patient_id
		self.name = name
		self.date = date
		self.type = "study"
		self.description = description

		print(name)


