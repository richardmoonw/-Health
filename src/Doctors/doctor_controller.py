class DoctorController:
	def validate_data(doctor):

		is_valid = True;

		if doctor.first_name is None:
			is_valid = False
		elif doctor.last_name is None:
			is_valid = False
		elif doctor.email is None:
			is_valid = False
		elif doctor.password is None:
			is_valid = False
		elif doctor.birthdate is None:
			is_valid = False
		elif doctor.phone is None:
			is_valid = False
		elif doctor.sex is None:
			is_valid = False
		elif doctor.school is None:
			is_valid = False
		elif doctor.graduation_date is None:
			is_valid = False
		elif doctor.speciality is None:
			is_valid = False
		elif doctor.hospital is None:
			is_valid = False

		return is_valid
