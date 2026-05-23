import time


class Delay:
    def __init__(self):
        self.start = time.time()
        
    def delay(self, seconds: float):
        """
        Run a busy loop until the seconds elapsed from the last call is reached.
        
        Returns
        -------
        (bool): True if time was delayed, False if there was delay exicuted
        """
        delayed = False
        while time.time() - self.start < seconds:
            delayed = True
            
        self.start = time.time()            
        return delayed