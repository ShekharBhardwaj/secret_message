from controller import Main
import os
import gc


class Runnable:
    is_runnable = True

    def run(self):
        os.system("clear")
        try:
            while self.is_runnable:
                main = Main()
                main.switch(main.start)
                print("Please secure your string, system will destroy your message upon refresh.")
                print("\n\n")
                rerun = input("More Encrypt/Decrypt ? Y/n: ").upper()
                os.system("clear")
                gc.enable()
                gc.collect()
                if rerun != "Y":
                    self.is_runnable = False
            else:
                print("Good bye...")
        except Exception as e:
            print("Something went wrong here, caused by: {}".format(e))


if __name__ == "__main__":
    running = Runnable()
    running.run()