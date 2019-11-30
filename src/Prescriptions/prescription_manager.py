class PrescriptionManager:
	def validate_prescription_information(treatment):
		is_valid = True

		if treatment.description is None:
			is_valid = False

		elif treatment.patient_id is None:
			is_valid = False

		elif treatment.doctor_id is None:
			is_valid = False

		elif treatment._type is None:
			is_valid = False

		elif treatment.date_created is None:
			is_valid = False

		elif treatment.dose is None:
			is_valid = False

		elif treatment.administration is None:
			is_valid = False

		elif treatment.frequency_value is None:
			is_valid = False

		elif treatment.frequency is None:
			is_valid = False

		return is_valid