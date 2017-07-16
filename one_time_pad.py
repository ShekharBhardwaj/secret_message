import logging

logging.getLogger().setLevel(logging.INFO)


def otp_shifts(sec_num_list, otp_received):
    """adjusts strings based on otp values"""
    print("sec_num sent2 otp : {}".format(sec_num_list))
    # checking if the otp's len is > than provided string
    if len(otp_received) > len(sec_num_list):
        otp_received = otp_received[1:len(sec_num_list)]
    index = 0
    # shifting letter's key's value based on OTP
    for num in otp_received:
        if len(sec_num_list) != index:
            otp_shift = int(num) + sec_num_list[index]
            del sec_num_list[index]
            sec_num_list.insert(index, otp_shift)
        index += 1
    logging.debug("After OTP {}".format(sec_num_list))
    print("numbers from OTP : {}".format(sec_num_list))
    return sec_num_list


class Otp:
    def __init__(self, otp):
        self.otp = otp

    def get_otp(self, choices_dict):
        """Spits out otp string after modifying it, list of negative integers for
        decryption, list positive integers for encryption"""
        # condition check for encryption and decryption
        if choices_dict.get("conversion_choice") == "D":
            neg_otp = [-num for num in self.otp]
            logging.debug(neg_otp)
            return neg_otp
        elif choices_dict.get("conversion_choice") == "E":
            logging.debug(self.otp)
            return self.otp



