#create the object from this

class connector:
    def __init__(self, signal1): #checking for one input
        self.signal1 = signal1

    def screen(self):
        if self.signal1 == 1:
            print("time started")
        elif self.signal1 == 0:
            print("time stopped")
        else:
            raise ("unknown signal received")