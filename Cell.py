class Cell:
    ID = 0

    def __init__(self, updateRate=0, color=None):
        self.color = color
        self.updateRate = updateRate
        self.updateTimeLeft = self.updateRate
        self.age = 0
        self.dormant = False
        self.failedUpdateAttempts = 0

    def update(self) -> bool:

        if self.dormant:
            return False

        if self.failedUpdateAttempts >= 2:
            self.dormant = True

        # decrease timer everytime
        self.updateTimeLeft -= 1
        
        # if timer is negative start again and return true
        if self.updateTimeLeft <= 0:
            self.updateTimeLeft = self.updateRate
            return True
        else:
            return False
    
    def awaken(self):
        self.dormant = False
        self.failedUpdateAttempts = 0