
class Move:

    def __init__(self,move,wMove,wComment,bMove,bComment,):
        self.move = move
        self.wMove = wMove
        self.wComment = wComment
        self.bMove = bMove
        self.bComment = bComment

    def __repr__(self):
        return f"({self.move}, {self.wMove}, {self.wComment}, {self.bMove}, {self.bComment})"
    
    #setters
    def setMove(self,move):
        self.move = move
    
    def setwMove(self,wMove):
        self.wMove = wMove

    def setwComment(self,wComment):
        self.wComment = wComment

    def setbMove(self,bMove):
        self.bMove = bMove

    def setbComment(self,bComment):
        self.bComment = bComment

    #getters
    def getMove(self):
        return self.move
    
    def getwMove(self):
        return self.wMove
    
    def getwComment(self):
        return self.wComment
    
    def getbMove(self):
        return self.bMove
    
    def getbComment(self):
        return self.bComment
