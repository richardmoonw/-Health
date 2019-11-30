#Class in charge of validating the degree of the doctor
class DocumentManager:
    def validate_degree(doctor):

            is_valid = True

            if doctor._id is None:
                is_valid = False

            elif doctor.filename is None:
                is_valid = False

            return is_valid