class AccountController:
	_id = 0
	first_name = ""
	last_name = ""
	email = ""
	password = ""
	birthdate = ""
	phone = ""
	sex = ""
	school = ""
	graduation_date = ""
	speciality = ""
	hospital = ""
	rating = 10
	filename = ""

	def enter_new_account_information(self, first_name, last_name, email, password, birthdate, phone, sex,\
				school, graduation_date, speciality, hospital):
	
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.birthdate = birthdate
		self.phone = phone
		self.sex = sex
		self.school = school
		self.graduation_date = graduation_date
		self.speciality = speciality
		self.hospital = hospital
		self.rating = 10

	
	# def create_degree(self, _id, filename):
	# 	self._id = _id
	# 	self.filename = filename


