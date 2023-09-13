
from Game import Game
from Move import Move
from WordCreation import WordCreation
import re
import pandas as pd
import statistics

#Here i create the new Game Collection objects
class GameCollection:
    
    
#Constructor-----------
    def __init__(self):
        self.games = []


# String---------------
    def __repr__(self):
        return f"GameCollection (code: {self.getGames()})"
        
    

# Setters--------------
    def setGames(self,games):
        self.games = games



# Getters--------------
    def getGames(self):
        return self.games
    
    

# Collecting data from Png file and creating a list of games


    def addGame(self,game):
        self.games.append(game)
        
    def collect_data(self,path): 
        file = open(path, 'r')
        pgn_data = file.read()

        games = list(filter(lambda x: len(x) > 0, pgn_data.split('\n\n[')))  #making a list with all the games
        
        for i, game in enumerate(games, start=1): 
            g = list(filter(lambda x: len(x) > 0, game.split('\n\n'))) #splitting the games into meta data and moves

            meta_data = g[0].splitlines() 
            
            this_dict = {}
            for line in meta_data:
                key,value = line.strip("[]").split(" ", maxsplit=1)
                this_dict[key] = value.strip('"')

            #meta data done

            moves = g[1].replace('\n', ' ') #making one long string of all the moves
            
            this_list = list(filter(lambda x: x, re.split(r'({[\w\W]*?})|\s', moves)))[:-1] #splitting all the moves and its 5 attributes into a list and removing the result (0-1)
        
            this_moves = []
            
            if len(this_list) % 5 == 0: #had to make two different for loops because of the different lengths of the last move
                for i in range(0, len(this_list), 5): 
                    attributes = this_list[i:i+5]
                    this_move = Move(*attributes)
                    this_moves.append(this_move)
            elif len(this_list) % 5 == 3:
                for i in range(0, len(this_list)-3, 5): 
                    attributes = this_list[i:i+5]
                    this_move = Move(*attributes)
                    this_moves.append(this_move)
                last_move = Move(this_list[-3], this_list[-2], this_list[-1], None, None)
                this_moves.append(last_move)

            game = Game() # adding the meta data and moves to the game object and adding it to the GC
            game.setMeta_data(this_dict)
            game.setMoves(this_moves)
            self.addGame(game)
    
        
    def write_data(self,path): #Exporting the data to a pgn file    
        file = open(path, 'w')
        for game in self.getGames():
            file.write("[Event \"" + game.getMeta_data()['Event'] + "\"]\n")
            file.write("[Site \"" + game.getMeta_data()['Site'] + "\"]\n")
            file.write("[Date \"" + game.getMeta_data()['Date'] + "\"]\n")
            file.write("[Round \"" + game.getMeta_data()['Round'] + "\"]\n")
            file.write("[White \"" + game.getMeta_data()['White'] + "\"]\n")
            file.write("[Black \"" + game.getMeta_data()['Black'] + "\"]\n")
            file.write("[Result \"" + game.getMeta_data()['Result'] + "\"]\n")
            file.write("[ECO \"" + game.getMeta_data()['ECO'] + "\"]\n")
            file.write("[WhiteElo \"" + game.getMeta_data()['WhiteElo'] + "\"]\n")
            file.write("[BlackElo \"" + game.getMeta_data()['BlackElo'] + "\"]\n\n")
            for move in game.getMoves():
                file.write(move.getMove())
                file.write(" ")
                file.write(move.getwMove())
                file.write(" ")
                file.write(move.getwComment())
                file.write(" ")
                if move.getbMove() != None:
                    file.write(move.getbMove())
                    file.write(" ")
                if move.getbComment() != None:
                    file.write(move.getbComment())
                    file.write(" ")
            file.write(game.getMeta_data()['Result'])
            file.write("\n\n")
        file.close()

    #Excel Functions------

    #load data from excel file
    def import_excel_data(self):
        df = pd.read_excel('ImportExcel.xlsx', sheet_name='Sheet1', header=None)
        df = df.fillna('')
        pgn_data = ''
        for row in df.values.tolist(): 
            for value in row:
                if isinstance(value, str):
                    pgn_data += value + '\n'
                elif isinstance(value, float):
                    pgn_data += str(int(value)) + '\n'
                else:
                    pass
        
        with open('Excel.pgn', 'w') as f:
            f.write(pgn_data)



    #export data to excel file
    def export_excel_data(self):
        with open('Excel.pgn', 'r') as f:
            pgn_data = f.read()
        pgn_rows = pgn_data.split('\n')
        df = pd.DataFrame(pgn_rows)
        df.to_excel('ExportExcel.xlsx', index=False, header=False, sheet_name='Sheet1', startrow=0, startcol=0)




    # Calculations --------

    def total_games(self):
        return len(self.getGames())

    def white_wins(self):
        wins = 0
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '1-0':
                wins += 1
        return wins
    
    def black_wins(self):
        wins = 0
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '0-1':
                wins += 1
        return wins
    
    def draws(self):
        draws = 0
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '1/2-1/2':
                draws += 1
        return draws

    #Stockfish Calculations
    def stockfish_wins(self):
        wins = 0
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '1-0':
                wins += 1
            elif game.getMeta_data()['Black'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '0-1':
                wins += 1
        return wins
    
    def stockfish_losses(self):
        losses = 0
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '0-1':
                losses += 1
            elif game.getMeta_data()['Black'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '1-0':
                losses += 1
        return losses
    
    def stockfish_draws(self):
        draws = 0
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '1/2-1/2':
                draws += 1
        return draws
    
    def stockfish_games_with_white(self):
        games = 0
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                games += 1
        return games

    def stockfish_wins_with_white(self):
        wins = 0
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '1-0':
                wins += 1
        return wins
    
    def stockfish_losses_with_white(self):
        losses = 0
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '0-1':
                losses += 1
        return losses
    
    def stockfish_draws_with_white(self):
        draws = 0
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '1/2-1/2':
                draws += 1
        return draws

    def stockfish_games_with_black(self):
        games = 0
        for game in self.getGames():
            if game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                games += 1
        return games
        
    def stockfish_wins_with_black(self):
        wins = 0
        for game in self.getGames():
            if game.getMeta_data()['Black'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '0-1':
                wins += 1
        return wins
    
    def stockfish_losses_with_black(self):
        losses = 0
        for game in self.getGames():
            if game.getMeta_data()['Black'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '1-0':
                losses += 1
        return losses
    
    def stockfish_draws_with_black(self):
        draws = 0
        for game in self.getGames():
            if game.getMeta_data()['Black'] == 'Stockfish 15 64-bit' and game.getMeta_data()['Result'] == '1/2-1/2':
                draws += 1
        return draws
    
    #Plotting calculations----------------
    def stockfish_move_list(self):
        move_list = []
        for i in range (0, 230):
            move_list.append(0)
        for game in self.getGames():
            for i in range (0, len(game.getMoves())):
                move_list[i] += 1
        return move_list
    
    def stockfish_move_list_white(self):
        move_list = []
        for i in range (0, 230):
            move_list.append(0)
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                for i in range (0, len(game.getMoves())):
                    move_list[i] += 1
        return move_list
    
    def stockfish_move_list_black(self):
        move_list = []
        for i in range (0, 230):
            move_list.append(0)
        for game in self.getGames():
            if game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                for i in range (0, len(game.getMoves())):
                    move_list[i] += 1
        return move_list
    
    def stockfish_move_list_wins(self):
        move_list = []
        for i in range (0, 230):
            move_list.append(0)
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '1-0' and game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                for i in range (0, len(game.getMoves())):
                    move_list[i] += 1
            if game.getMeta_data()['Result'] == '0-1' and game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                for i in range (0, len(game.getMoves())):
                    move_list[i] += 1
        return move_list
    
    def stockfish_move_list_losses(self):
        move_list = []
        for i in range (0, 230):
            move_list.append(0)
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '0-1' and game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                for i in range (0, len(game.getMoves())):
                    move_list[i] += 1
            if game.getMeta_data()['Result'] == '1-0' and game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                for i in range (0, len(game.getMoves())):
                    move_list[i] += 1
        return move_list
    

    #mean----------------
    def stockfish_mean(self):
        move_list = []
        for game in self.getGames():
            move_list.append(len(game.getMoves()))
        return round(statistics.mean(move_list),2)
    
    def stockfish_mean_white(self):
        move_list = []
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
        return round(statistics.mean(move_list),2)
    
    def stockfish_mean_black(self):
        move_list = []
        for game in self.getGames():
            if game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
        return round(statistics.mean(move_list),2)
    
    def stockfish_mean_wins(self):
        move_list = []
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '1-0' and game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
            if game.getMeta_data()['Result'] == '0-1' and game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
        return round(statistics.mean(move_list),2)
    
    def stockfish_mean_losses(self):
        move_list = []
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '0-1' and game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
            if game.getMeta_data()['Result'] == '1-0' and game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
        return round(statistics.mean(move_list),2)
            


    #standard deviation---------------- 
    def stockfish_SD(self):
        move_list = []
        for game in self.getGames():
            move_list.append(len(game.getMoves()))
        return round(statistics.stdev(move_list),2)

    def stockfish_SD_white(self):
        move_list = []
        for game in self.getGames():
            if game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
        return round(statistics.stdev(move_list),2)
    
    def stockfish_SD_black(self):
        move_list = []
        for game in self.getGames():
            if game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
        return round(statistics.stdev(move_list),2)
    
    def stockfish_SD_wins(self):
        move_list = []
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '1-0' and game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
            if game.getMeta_data()['Result'] == '0-1' and game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
        return round(statistics.stdev(move_list),2)
    
    def stockfish_SD_losses(self):
        move_list = []
        for game in self.getGames():
            if game.getMeta_data()['Result'] == '0-1' and game.getMeta_data()['White'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
            if game.getMeta_data()['Result'] == '1-0' and game.getMeta_data()['Black'] == 'Stockfish 15 64-bit':
                move_list.append(len(game.getMoves()))
        return round(statistics.stdev(move_list),2)
    
        

        


# Main-------------------
def main():
        games1 = GameCollection()
        games1.collect_data('PGN/GameList.pgn')
        word = WordCreation()
        word.create_word_document(games1)
main()  