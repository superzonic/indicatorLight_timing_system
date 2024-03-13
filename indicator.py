#create the object from this
import time
import input_output_tester

import input_output_tester
class connector:
    def __init__(self, signal1): #checking for one input
        self.signal1 = signal1

    def screen(self):
        if self.signal1 == 1:
            print("time started")
        elif self.signal1 == 0:
            print("time stopped")
        else:
            print(self.signal1)
            raise ("unknown signal received")

while True:
    time.sleep(1)
    x = input_output_tester.button_press()
    tes = connector(int(x))
    tes.screen()
