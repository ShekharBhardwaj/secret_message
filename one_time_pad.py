import logging

logging.getLogger().setLevel(logging.INFO)


class Otp:
    def __init__(self, otp):
        self.otp = otp

    def get_otp(self, choices_dict):
        if choices_dict.get("conversion_choice") == "E":
            neg_otp = [-num for num in self.otp]
            logging.info(neg_otp)
            return neg_otp
        elif choices_dict.get("conversion_choice") == "D":
            logging.info(self.otp)
            return self.otp
