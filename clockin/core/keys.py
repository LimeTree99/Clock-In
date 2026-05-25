

class Keys:
    def __init__(self, window):
        self.window = window
        self.last = ""
        
        self.window.nodelay(True)
        
    def update(self):
        try:
            self.last = self.window.getkey()
        except:
            pass
        
    def usekey(self):
        "returns keystring and resets it to an empty string"
        keystring = self.last
        self.last = ""
        return keystring