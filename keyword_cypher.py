from cipher import Cipher
import logging
import csv


logging.getLogger().setLevel(logging.INFO)


class Keyword(Cipher):

    dyc_string = []
    enc_string = []
    sec_kw_dict = {}
    secret_numbers = []
    otp_enabled = []

    def __init__(self, secret_string, otp, *args, **kwargs):
        super().__init__(secret_string)
        self.otp = otp

    def get_secret_numbers(self, switch_dict):
        """spits out secret number after applying otp."""
        logging.debug("in Keyword sec_kw_dict {}".format(self.sec_kw_dict))
        # Generating secret number based on alphabet position
        # in fed csv file and returning the position numbers.
        logging.debug("Secret string in Keyword: {}s".format(self.secret_string))
        for letter in self.secret_string:
            self.secret_numbers.append(switch_dict.get(letter))
        logging.debug("Before OTP {}".format(self.secret_numbers))
        # Adjusting positions based on OTP provided by Agent.
        if len(self.otp) > len(self.secret_numbers):
            self.otp = self.otp[1:len(self.secret_numbers)]
        index = 0
        for num in self.otp:
            if len(self.secret_numbers) != index:
                otp_shift = num + int(self.secret_numbers[index])
                del self.secret_numbers[index]
                self.secret_numbers.insert(index, str(otp_shift))
            index += 1
        logging.debug("After OTP {}".format(self.secret_numbers))
        return self.secret_numbers

    @property
    def encrypt(self):
        """encrypts the string"""
        with open("keyword_assignation.csv", "r") as keyword_csv:
            reader_ekw = csv.DictReader(keyword_csv)
            for row in reader_ekw:
                for k, v in row.items():
                    self.sec_kw_dict[k] = v
        # Looping through all the secret numbers,
        # numbers here are based on secret cipher positioning
        for num in self.get_secret_numbers(self.sec_kw_dict):
            # Encrypting data based on letter's position
            # in cipher based original csv secret numbers
            for k, v in self.get_orig_dict().items():
                if num == v:
                    self.enc_string.append(k)
        return ''.join(self.enc_string)

    @property
    def decrypt(self):
        """decrypts the string"""
        # opening csv
        with open("keyword_assignation.csv", "r") as decrypt_csv:
            reader_dkw = csv.DictReader(decrypt_csv)
            for row in reader_dkw:
                for k, v in row.items():
                    self.sec_kw_dict[k] = v
        logging.debug("secret number length in decrypt: {}".
                      format(len(self.secret_numbers)))
        # looping through original csv dict
        for num in self.get_secret_numbers(self.get_orig_dict()):
            for k, v in self.sec_kw_dict.items():
                if num == v:
                    self.dyc_string.append(k)
            space_adjust_list = [" " if letter == "_" else letter for letter in self.dyc_string]
        return ''.join(space_adjust_list)


if __name__ == "__main__":
    key = Keyword(["A", "B", "C", " ", "D"])
    print(key.encrypt)
    print(key.decrypt)