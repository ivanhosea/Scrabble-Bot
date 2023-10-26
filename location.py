class Location:
    def __init__(self, X, Y, X_END, Y_END):
        self.X = X
        self.Y = Y
        self.X_END = X_END
        self.Y_END = Y_END
    
    # Check if the entity in this location is clicked
    def isClicked(self, x, y):
        if x >= self.X and x < self.X_END and y >= self.Y and y <= self.Y_END:
            return True
        return False