import cipher
import one_time_pad
import logging
import re

logging.getLogger().setLevel(logging.INFO)


class Main:
    cipher_avail = ["KEYWORD", "IMPOSITION"]
    agent_name = input("State your field name:")
    welcome = "Welcome Agent {}, please select the cipher, i,e 0, 1, 2.. etc".format(agent_name)

    def __init__(self):
        pass

    @property
    def no_such_cipher_found(self):
        raise ValueError("No such cipher found")

    @property
    def start(self):
        print(self.welcome)
        for count in range(len(self.cipher_avail)):
            print("{}: ".format(count)+self.cipher_avail[count].title())
        cipher_choice = input("Enter your choice: ")
        if len(cipher_choice) != 1:
            raise "Please enter valid cipher choice"
        conversion_choice = input("What do you want to do today (E)ncryption or (D)ecryption, E/D: ").upper()
        conversion_string = input("You Secret message: ").upper()
        user_otp = input("Enter your OTP: ")
        fiver_display = input("Do you want to handle in block of 5 (y/N): ").upper()
        if fiver_display != "Y":
            fiver_display = "N"
        choices_dict = {"cipher_choice": cipher_choice,
                        "conversion_choice": conversion_choice,
                        "conversion_string": conversion_string,
                        "user_otp": user_otp,
                        "fiver_display": fiver_display}
        return choices_dict

    def block_of_five(self, sec_str):
        first_fives = re.findall('.....', sec_str)
        reminder = sec_str[:-len(sec_str)%5:]
        final_str = first_fives.append(reminder)
        print(final_str)
        return final_str

    def remove_blocks_of_five(self, enc_str):
        enc_str_list = list(enc_str)
        print(enc_str_list)
        space_removed_str = "".join(["" if letter == " " else letter for letter in enc_str_list])
        print(space_removed_str)
        return space_removed_str

    def keyword(self, choices_dict):
        print("You have selected {}, awesome choice.".format(choices_dict.get("cipher_choice")))
        con_cho = choices_dict.get("conversion_choice")
        con_str = list(choices_dict.get("conversion_string"))
        usr_otp = list(choices_dict.get("user_otp"))
        if con_cho == "E":
            kw = cipher.Keyword(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).get_otp(choices_dict))
            if choices_dict.get("fiver_display") == "N":
                print("Your encrypted message: {}".format(kw.encrypt))
            else:
                print(" ".join(self.block_of_five(kw.encrypt)))

        elif con_cho == "D":
            if choices_dict.get("fiver_display") == "N":
                kw = cipher.Keyword(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).get_otp(choices_dict))
            else:
                kw = cipher.Keyword(self.remove_blocks_of_five(con_str), one_time_pad.Otp([int(num) for num in usr_otp]).get_otp(choices_dict))
            print("Your decrypted message: {}".format(kw.decrypt))
        else:
            raise ValueError("'{}' is not a valid choice, you can either (E)ncrypt or (D)ecrypt.".format(con_cho))

    # def switch(self, choices_dict):
    #     switch_dict = {"0": self.keyword(choices_dict)}
    #     logging.info("Cipher choice : {}".format(choices_dict.get("cipher_choice")))
    #     switch_dict.get(choices_dict.get("cipher_choice"))

    def switch(self, choices_dict):
        if choices_dict.get("cipher_choice") == "0":
            self.keyword(choices_dict)
        elif choices_dict.get("cipher_choice") == "1":
            raise NotImplementedError("This Cipher is not Implemented yet.")
        else:
            raise ValueError("{}, is not a valid cipher, please select only the exiting cipher code".format(choices_dict.get("cipher_choice")))












if __name__ == "__main__":
    main = Main()
    main.switch(main.start)



