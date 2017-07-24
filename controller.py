import keyword_cypher as keyword
import affine_cypher as affine
import atbash_cypher as atbash
import one_time_pad
import logging
import re

logging.getLogger().setLevel(logging.INFO)


class Main:
    cipher_avail = ["KEYWORD", "AFFINE", "ATBASH"]
    agent_name = input("State your field name:")
    print("\n")
    welcome = "Welcome Agent {}, please select the cipher, i,e 0, 1, 2.. etc".format(agent_name)

    def __init__(self):
        pass

    @property
    def no_such_cipher_found(self):
        """
        :raise ValueError
        """
        raise ValueError("No such cipher found")

    @property
    def start(self):
        """
        creates a dictionary based on users's Q&A
        :return: choice_dict
        """
        print(self.welcome)
        for count in range(len(self.cipher_avail)):
            print("{}: ".format(count)+self.cipher_avail[count].title())
        print("\n\n")
        cipher_choice = input("Enter your choice: ")
        print("\n")
        if len(cipher_choice) != 1:
            raise "Please enter valid cipher choice"
        conversion_choice = input("What do you want to do today (E)ncryption or (D)ecryption, E/D: ").upper()
        conversion_string = input("You Secret message string: ")
        user_otp = input("Enter your OTP numerics: ")
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
        """
        string divided in 5 words separated by space
        :param sec_str:
        :return: first_fives
        """
        first_fives = re.findall('.....', sec_str)
        mod = len(sec_str) % 5
        reminder = "".join(sec_str[-mod:])
        first_fives.append(reminder)
        return first_fives

    def remove_blocks_of_five(self, enc_str):
        """
        removes spaces within the string
        :param enc_str:
        :return: space_removed_str
        """
        enc_str_list = list(enc_str)
        space_removed_str = "".join(["" if letter == " " else letter for letter in enc_str_list])
        return space_removed_str

    def keyword(self, choices_dict):
        """
        This is keyword controller
        :param choices_dict:
        """
        print("You have selected {}, awesome choice.".
              format(self.cipher_avail[int(choices_dict.get("cipher_choice"))]))
        con_cho = choices_dict.get("conversion_choice")
        usr_otp = list(choices_dict.get("user_otp"))
        # condition for encryption
        if con_cho == "E":
            con_str = list(choices_dict.get("conversion_string").upper())
            kw = keyword.Keyword(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).
                                 get_otp(choices_dict))
            if choices_dict.get("fiver_display") == "N":
                print("Your encrypted message: {}".format(kw.encrypt))
            else:
                print("Your encrypted message: {}".format(" ".join(self.block_of_five(kw.encrypt))))
        # condition for decryption
        elif con_cho == "D":
            con_str = list(choices_dict.get("conversion_string"))
            if choices_dict.get("fiver_display") == "N":
                kw = keyword.Keyword(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).
                                     get_otp(choices_dict))
            else:
                space_removed = self.remove_blocks_of_five(con_str)
                kw = keyword.Keyword(space_removed,
                                     one_time_pad.Otp([int(num) for num in usr_otp]).
                                     get_otp(choices_dict))
            # TODO: possible memory leak find out why ?
            print("Your decrypted message: {}".
                  format(kw.decrypt[:len(space_removed)]))
        else:
            raise ValueError("'{}' is not a valid choice, you can either (E)ncrypt or (D)ecrypt.".
                             format(con_cho))

    def affine(self, choices_dict):
        """
        This is Affine controller
        :param choices_dict:
        """
        print("You have selected {}, awesome choice.".
              format(self.cipher_avail[int(choices_dict.get("cipher_choice"))]))
        con_cho = choices_dict.get("conversion_choice")
        usr_otp = list(choices_dict.get("user_otp"))
        # condition for encryption
        if con_cho == "E":
            con_str = list(choices_dict.get("conversion_string").upper())
            aff = affine.Affine(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).
                                get_otp(choices_dict))
            if choices_dict.get("fiver_display") == "N":
                print("Your affine encrypted message: {}".
                      format(aff.encrypt))
            else:
                print("Your affine encrypted message: {}".
                      format(" ".join(self.block_of_five(aff.encrypt))))
        # condition for decryption
        elif con_cho == "D":
            con_str = list(choices_dict.get("conversion_string").upper())
            if choices_dict.get("fiver_display") == "N":
                aff = affine.Affine(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).
                                    get_otp(choices_dict))
            else:
                space_removed = self.remove_blocks_of_five(con_str)
                aff = affine.Affine(space_removed,
                                    one_time_pad.Otp([int(num) for num in usr_otp]).
                                    get_otp(choices_dict))
            print("Your decrypted message: {}".format(aff.decrypt))
        else:
            raise ValueError("'{}' is not a valid choice, you can either (E)ncrypt or (D)ecrypt.".
                             format(con_cho))

    def atbash(self, choices_dict):
        """
        This is Atbash controller
        :param choices_dict:
        """
        print("You have selected {}, awesome choice.".
              format(self.cipher_avail[int(choices_dict.get("cipher_choice"))]))
        con_cho = choices_dict.get("conversion_choice")
        usr_otp = list(choices_dict.get("user_otp"))
        # condition for encryption
        if con_cho == "E":
            con_str = list(choices_dict.get("conversion_string").upper())
            atb = atbash.Atbash(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).
                                get_otp(choices_dict))
            if choices_dict.get("fiver_display") == "N":
                print("Your affine encrypted message: {}".format(atb.encrypt))
            else:
                print("Your affine encrypted message: {}".
                      format(" ".join(self.block_of_five(atb.encrypt))))
        # condition for decryption
        elif con_cho == "D":
            con_str = list(choices_dict.get("conversion_string").upper())
            if choices_dict.get("fiver_display") == "N":
                atb = atbash.Atbash(con_str, one_time_pad.Otp([int(num) for num in usr_otp]).
                                    get_otp(choices_dict))
            else:
                atb = atbash.Atbash(self.remove_blocks_of_five(con_str),
                                    one_time_pad.Otp([int(num) for num in usr_otp]).
                                    get_otp(choices_dict))
            print("Your decrypted message: {}".format(atb.decrypt))
        else:
            raise ValueError("'{}' is not a valid choice, you can either (E)ncrypt or (D)ecrypt.".
                             format(con_cho))

    def switch(self, choices_dict):
        """
        Makes the cypher type switch based on user's choce
        :param choices_dict:
        :return:
        """
        # condition to execute the cypher
        if choices_dict.get("cipher_choice") == "0":
            self.keyword(choices_dict)
        elif choices_dict.get("cipher_choice") == "1":
            self.affine(choices_dict)
        elif choices_dict.get("cipher_choice") == "2":
            self.atbash(choices_dict)
        else:
            raise ValueError("{}, is not a valid cipher, please select only the exiting cipher code"
                             .format(choices_dict.get("cipher_choice")))


if __name__ == "__main__":
    main = Main()
    main.switch(main.start)



