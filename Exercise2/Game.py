
class Game:
        
    def __init__(self):
        self.meta_data = {}
        self.moves = []

    def __repr__(self):
         return f"ChessGame({self.meta_data}, {self.moves})"
    
    #setters
    def setMeta_data(self, meta_data):
        self.meta_data = meta_data

    def setMoves(self, moves):
        self.moves = moves

    #getters
    def getMeta_data(self):
        return self.meta_data
    
    def getMoves(self): 
        return self.moves
    


