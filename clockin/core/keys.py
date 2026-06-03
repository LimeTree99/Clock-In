

class Keys:
    KEY_ENTER = 10
    KEY_PADENTER = 459
    def __init__(self, window):
        self.window = window
        self.last = -1
        
        self.window.keypad(True)
        self.window.nodelay(True)
        
    def update(self):
        self.last = self.window.getch()
        
    def usekey(self):
        "returns keyconst and resets self.last to -1"
        keyconst = self.last
        self.last = -1
        return keyconst