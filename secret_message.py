import cipher
import one_time_pad
import logging

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
        conversion_choice = input("What do you want to do today (E)ncryption or (D)ecryption, E/D: ").upper()
        conversion_string = input("You Secret message: ").upper()
        user_otp = input("Enter your OTP: ")
        choices_dict = {"cipher_choice": cipher_choice,
                        "conversion_choice": conversion_choice,
                        "conversion_string": conversion_string,
                        "user_otp": user_otp}
        return choices_dict

    def keyword(self, choices_dict):
        print("You have selected {}, awesome choice.".format(choices_dict.get("cipher_choice")))
        con_cho = choices_dict.get("conversion_choice")
        con_str = choices_dict.get("conversion_string")
        usr_otp = list(choices_dict.get("user_otp"))
        if con_cho == "E":
            try:
                kw = cipher.Keyword(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).get_otp(choices_dict))
            except TypeError or ValueError as error:
                print("Error caused by : {}".format(error))
            print("Your encrypted message: {}".format(kw.encrypt))
        elif con_cho == "D":
            try:
                kw = cipher.Keyword(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).get_otp(choices_dict))
            except TypeError or ValueError as error:
                print("Error caused by : {}".format(error))
            print("Your decrypted message: {}".format(kw.decrypt))
        else:
            raise ValueError("'{}' is not a valid choice, you can either (E)ncrypt or (D)ecrypt.".format(con_cho))

    def switch(self, choices_dict):
        switch_dict = {'0': self.keyword(choices_dict)}
        logging.info("Cipher choice : {}".format(choices_dict.get("cipher_choice")))
        return switch_dict.get(choices_dict.get("cipher_choice"))














main = Main()
main.switch(main.start)


