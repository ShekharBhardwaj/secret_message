from cipher import Cipher
import logging as logger
import one_time_pad as pad

logger.getLogger().setLevel(logger.DEBUG)

originals = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11, "M": 12,
             "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24,
             "Z": 25, "_": 26, "!": 27, "@": 28, "#": 29, "$": 30, "%": 31, "^": 32, "&": 33, "*": 34, "?": 35}

atbash_originals = {0: "Z", 1: "Y", 2: "X", 3: "W", 4: "V", 5: "U", 6: "T", 7: "S", 8: "R", 9: "Q", 10: "P", 11: "O",
                    12: "N", 13: "M", 14: "L", 15: "K", 16: "J", 17: "I", 18: "H", 19: "G", 20: "F", 21: "E", 22: "D",
                    23: "C", 24: "B", 25: "A", 26: "_", 27: "!", 28: "@", 29: "#", 30: "$", 31: "%", 32: "^", 33: "&",
                    34: "*", 35: "?"}


class Atbash(Cipher):
    def __init__(self, secret_string, otp):
        self.secret_string = secret_string
        super().__init__(self.secret_string)
        self.otp = otp

    @property
    def encrypt(self):
        """
        encrypts the string
        :return:
        """
        sec_letters = []
        atb_index = []
        sec_string_list = []
        for letter in self.secret_string:
            # getting value from orig dict
            orig_indx = originals.get(letter)
            # getting value from atbash dict
            atbash_sec_letters = atbash_originals.get(orig_indx)
            sec_letters.append(atbash_sec_letters)
        for atbash_datum in sec_letters:
            for k, v in atbash_originals.items():
                if v == atbash_datum:
                    atb_index.extend([k])

        # making otp shift
        otp_shifted_index = pad.otp_shifts(atb_index, self.otp)
        for datum in otp_shifted_index:
            sec_string_list.extend(atbash_originals.get(datum))
        return ''.join(sec_string_list)

    @property
    def decrypt(self):
        """
        decrypts the string
        :return:
        """
        incoming_atbash_index = []
        adjusted_atbash_letters = []
        # getting keys from atbash dict
        for letter in self.secret_string:
            for k, v in atbash_originals.items():
                if v == letter:
                    incoming_atbash_index.append(k)
        otp_adjusted_index = pad.otp_shifts(incoming_atbash_index, self.otp)

        # adjusting otp shift
        for adjusted_index in otp_adjusted_index:
            for k, v in originals.items():
                if v == adjusted_index:
                    adjusted_atbash_letters.append(k)
        return ''.join(adjusted_atbash_letters)

