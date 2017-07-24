from cipher import Cipher
import logging
import one_time_pad as pad

logging.getLogger().setLevel(logging.INFO)

originals = {":": 0, "A": 1, "B": 2, "C": 3, "D": 4,
             "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
             "J": 10, "K": 11, "L": 12, "M": 13, "N": 14,
             "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
             "T": 20, "U": 21, "V": 22, "W": 23, "X": 24,
             "Y": 25, "Z": 26, "_": 27, "!": 28, "@": 29,
             "#": 30, "$": 31, "%": 32, "^": 33, "&": 34,
             "*": 35, "?": 36}


class Affine(Cipher):
    def __init__(self, secret_string, otp, *args, **kwargs):
        self.secret_string = secret_string
        super().__init__(self.secret_string)
        self.otp = otp
        logging.debug(self.otp)

    def e_numlogix(self, sec_str):
        """
        Convert string into secret number
        :param sec_str:
        :return:
        """
        # Applying (a x datum + b) mod 26
        num = originals.get(sec_str)
        if num == 27:
            return 27
        else:
            return (5*num+8) % 26

    def e_strlogix(self, num):
        """converts secret number into secret letter"""
        # matching num to corresponding letter
        for key, value in originals.items():
            if num == value:
                return key

    def d_numlogix(self, datum):
        """
        matching letter to it's original number
        :param datum:
        :return:
        """
        return originals.get(datum)

    def d_strlogix(self, dec_num):
        """
        matching decrypted letter's number to it's letter and returning decrypted string
        :param dec_num:
        :return:
        """
        real_nums = []
        real_str_list = []
        # applying reverse formula to get actual value from received number
        for datum in dec_num:
            if datum == 27:
                mod_num = 27
            else:
                mod_num = 21 * (datum - 8) % 26
            real_nums.append(mod_num)
        # retrieving real letters of string from original dict
        for datum in real_nums:
            real_str_list.append(self.e_strlogix(datum))
        index = 0
        for datum in real_str_list:
            if datum == "_":
                del real_str_list[index]
                real_str_list.insert(index, " ")
            index += 1
        return real_str_list

    @property
    def encrypt(self):
        """
        encrypts received string
        :return:
        """
        sec_num_list = pad.otp_shifts([self.e_numlogix(datum) for datum in self.secret_string], self.otp)
        encrypted_list_str = [self.e_strlogix(datum) for datum in sec_num_list]
        return ''.join(encrypted_list_str)

    @property
    def decrypt(self):
        """
        decrypts received string
        :return:
        """
        num_list = pad.otp_shifts([self.d_numlogix(datum) for datum in self.secret_string], self.otp)
        de_list_str = self.d_strlogix(num_list)
        return ''.join(de_list_str)


if __name__ == "__main__":
    aff = Affine(['S', 'H', 'E', 'K', 'H', 'A', 'R'], [2, 2, 3])
    print(aff.encryption())
    aff1 = Affine(aff.encryption(), [-2, -2, -3])
    print(aff1.decryption())

