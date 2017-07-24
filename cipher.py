import csv
import logging


logging.getLogger().setLevel(logging.INFO)


class Cipher:
    """
    Super class
    """
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
        # Reading original positions from user fed csv file.
        with open("original_assigned.csv", "r") as orig_csv:
            reader = csv.DictReader(orig_csv)
            for row in reader:
                # Creating dicts from csv data
                for k, v in row.items():
                    self.orig_dict[k] = v

    def encrypt(self):
        raise NotImplementedError()

    def decrypt(self):
        raise NotImplementedError()

    # Returns dict for original positions for messages
    def get_orig_dict(self):
        return self.orig_dict






