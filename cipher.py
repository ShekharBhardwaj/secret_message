import csv
import logging


logging.getLogger().setLevel(logging.INFO)


class Cipher:

    orig_dict = {}

    def __init__(self, secret_string, *args, **kwargs):
        # Checking the length of secret string list.

        if len(secret_string) < 1:
            raise ValueError("Secret string cannot be empty")
        self.secret_string = secret_string
        self.index = 0
        for letter in self.secret_string:
            if letter == " ":
                del self.secret_string[self.index]
                self.secret_string.insert(self.index, "_")
            self.index += 1

        logging.info("Secret string in Cipher: {}".format(self.secret_string))
        # Reading original positions from user fed csv file.
        with open("original_assigned.csv", "r") as orig_csv:
            reader = csv.DictReader(orig_csv)
            for row in reader:
                # Creating dicts from csv data
                for k, v in row.items():
                    self.orig_dict[k] = v
        logging.info("in Cipher __init__ orig.dict {}".format(self.orig_dict))

    # Returns dict for original positions for messages
    def get_orig_dict(self):
        return self.orig_dict


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
        logging.info("in Keyword sec_kw_dict {}".format(self.sec_kw_dict))
        # Generating secret number based on alphabet position in fed csv file and returning the position numbers.
        logging.info("Secret string in Keyword: {}s".format(self.secret_string))
        for letter in self.secret_string:
            self.secret_numbers.append(switch_dict.get(letter))
        logging.info("Before OTP {}".format(self.secret_numbers))
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
        logging.info("After OTP {}".format(self.secret_numbers))
        return self.secret_numbers

    @property
    def encrypt(self):
        with open("keyword_assignation.csv", "r") as keyword_csv:
            reader_ekw = csv.DictReader(keyword_csv)
            for row in reader_ekw:
                for k, v in row.items():
                    self.sec_kw_dict[k] = v
            # self.sec_kw_dict[" "] = "27"
            # logging.info("keyword dict")
            # logging.info(self.sec_kw_dict)
        # Looping through all the secret numbers, numbers here are based on secret cipher positioning
        for num in self.get_secret_numbers(self.sec_kw_dict):
            # Encrypting data based on letter's position in cipher based original csv secret numbers
            for k, v in self.get_orig_dict().items():
                if num == v:
                    self.enc_string.append(k)
        return ''.join(self.enc_string)

    @property
    def decrypt(self):
        with open("keyword_assignation.csv", "r") as decrypt_csv:
            reader_dkw = csv.DictReader(decrypt_csv)
            for row in reader_dkw:
                for k, v in row.items():
                    self.sec_kw_dict[k] = v
            # self.sec_kw_dict["_$_"] = "27"
            # logging.info(self.kw_dict)
        logging.info("secret number length in decrypt: {}".format(len(self.secret_numbers)))
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