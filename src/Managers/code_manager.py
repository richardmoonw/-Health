class CodeManager:
	def validate_code(patient):

		is_valid = True

		if patient._id is None:
			is_valid = False

		return is_valid