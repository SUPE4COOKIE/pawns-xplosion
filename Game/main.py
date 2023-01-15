import tkinter as tk
from Game.Tile import Tile # import the tile class for the module (anything tile related)
from random import choice # used to choose a random tile for the computer
from os import remove # used to remove the save file
import json # we use json to save our game state
# we use base64 to encode our save file
from base64 import b64encode, b64decode # not the best option but none would be perfect since it could be easily decoded with source code

class game:
    def __init__(self, BOX_SIZE=100, TITLE="Pawns-Xplosion") -> None:
        # constants
        self.BOX_SIZE : int = BOX_SIZE
        self.COLORS = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "white"] #colors for the players

        # data for initialization
        self.computer : bool = self.AskIfComputer() # ask if the user wants to play against computer
        self.PLAYER_COUNT : int = 2 if self.computer else self.AskPlayerCount() #ask for the number of players
        self.COLUMN, self.ROW = self.AskColumnRow() # ask for the number of columns and rows
        self.WIDTH : int = BOX_SIZE*self.COLUMN # width of the window
        self.HEIGHT : int = BOX_SIZE*self.ROW # height of the window

        # data used in the game
        self.eliminated_players = [] # list of eliminated players
        self.player = 0 # current player
        self.game_over = False # is the game over?
        
        # anything tkinter needs
        self.window = tk.Tk() # window
        self.canvas = tk.Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT, bg="blue", highlightbackground="black") # main canvas
        self.tiles = [[Tile(self.BOX_SIZE,self.canvas , self.SetCapacity(x, y),x,y,self.ClickListener) for y in range(self.ROW)]
                  for x in range(self.COLUMN)] # list of tiles
        self.window.title(TITLE) # title of the window
        self.window.resizable(False, False) # set the window to be non-resizable
        self.canvas.pack() # pack the canvas

    def AskIfComputer(self) -> bool:
        """
        Asks the user if he wants to play against computer
        """
        while True:
            user_input = input(
                "Do you want to play against computer? (y/n): ")
            if user_input == "y":
                return True
            elif user_input == "n":
                return False
            print("Invalid input. Try again.")

    def AskPlayerCount(self) -> int:
        """
        Asks the user for the number of players
        """
        while True:
            user_input = input(
                "Enter the number of player (between 2 and 8): ")
            num = int(user_input) if user_input.isdigit() else None
            if num and 2 <= num <= 8:
                return num
            print("Invalid input. Try again.")

    def AskColumnRow(self) -> tuple[int, int]:
        """
        Asks the user for the number of columns and rows
        """
        while True:
            user_input = input(
                "Enter the number of Columns (between 3 and 12): ")
            Column = int(user_input) if user_input.isdigit() else None
            if Column and 3 <= Column <= 12:
                while True:
                    user_input = input(
                        "Enter the number of Rows (between 3 and 10): ")
                    Row = int(user_input) if user_input.isdigit() else None
                    if Row and 3 <= Row <= 10:
                        return Column, Row
                    print("Invalid input. Try again.")
            print("Invalid input. Try again.")

    def IsGameOver(func):
        """
        decorator that checks if the game is over before executing the function
        """
        def wrapper(self, *args, **kwargs):
            if not self.game_over:
                return func(self, *args, **kwargs)
        return wrapper
    
    def IsTileOwner(func):
        """
        decorator that checks if the tile is owned by the current player before executing the function
        """
        def wrapper(self,*args,**kwargs):
            if self.tiles[args[0]][args[1]].owner == None or self.tiles[args[0]][args[1]].owner == self.COLORS[self.player]:
                return func(self,*args,**kwargs)
        return wrapper
    
    @IsGameOver
    def SaveGameState(self) -> None:
        """
        Saves the game state to the "save" file and encodes it with base64
        """
        json_data = {"pos":[],
                    "player":self.player,
                    "eliminated_players":self.eliminated_players
                    } # data to be saved
        # data gathering
        for i in self.tiles:
            for tile in i:
                json_data["pos"].append((tile.pawns,tile.owner))

        json_data = json.dumps(json_data) # convert the data to json
        with open("save", "w") as f:
            f.write(b64encode(json_data.encode()).decode()) # encode the data and write it to the file

    
    def LoadGameState(self) -> None:
        """
        Loads the game state from the "save" file and decodes it with base64
        (save file from an unfinished game)
        """
        try: # try to load the game state from the "save" file and decode it with base64 
            with open("save", "r") as f:
                json_data = json.loads(b64decode(f.read().encode()).decode()) # decode the data and convert it to json
                self.player = json_data["player"] - 1 if json_data["player"] != 0 else self.PLAYER_COUNT - 1 # set the player to the previous player to then update it
                self.eliminated_players = json_data["eliminated_players"] # set the eliminated players

                for i in range(len(self.tiles)): # set the pawns and owners of the tiles
                    for j in range(len(self.tiles[i])):
                        self.tiles[i][j].SetPawns(json_data["pos"][i*len(self.tiles[i])+j][0],json_data["pos"][i*len(self.tiles[i])+j][1]) # set the pawns and owner of the tile
            self.CheckPawnOwnerState() # just to be sure that the game isn't finished or if some players are eliminated
            self.ChangePlayer() # update player
        except FileNotFoundError: # if the file doesn't exist, just pass and start from 0
            pass
        

    def SetCapacity(self, x, y) -> int:
        """
        Sets the max capacity of the tile based on its position
        """
        # corners
        if (x == 0 and y == 0) or (x == 0 and y == self.ROW-1) or (x == self.COLUMN-1 and y == 0) or (x == self.COLUMN-1 and y == self.ROW-1):
            return 1
        # edges
        elif x == 0 or y == 0 or x == self.COLUMN-1 or y == self.ROW-1:
            return 2
        # anything else
        return 3
    
    
    def GetNeighbours(self, x, y) -> list[Tile]:
        """
        return direct neighbours (no border)
        """
        neighbours = [] # list of neighbours

        # add the neighbours to the list based on the main tile position
        if x > 0:
            neighbours.append(self.tiles[x-1][y])
        if x < self.COLUMN-1:
            neighbours.append(self.tiles[x+1][y])
        if y > 0:
            neighbours.append(self.tiles[x][y-1])
        if y < self.ROW-1:
            neighbours.append(self.tiles[x][y+1])
        return neighbours

    @IsTileOwner # check if the tile is owned by the current player
    @IsGameOver # check if the game is over
    def ClickListener(self, x,y) -> None:
        """
        Function called when a tile is clicked
        manage the calls to the following functions :
            - the explosion
            - the change of player
            - the saving of the game state
            - the computer play
        """
        tile = self.tiles[x][y] # get the tile that has been clicked

        if tile.SetPawns(tile.pawns+1, self.COLORS[self.player]) == False: # if the tile is full
            tile.ClearPawns() # clear the tile
            self.Explosion(x,y) # explode

        self.CheckPawnOwnerState() # check if the game is over or if some players are eliminated
        self.ChangePlayer() # change the player turn
        self.SaveGameState() # save the game state

        if self.computer: # if the computer is playing
            self.ComputerPlay() # play for the computer
    
    @IsGameOver
    def Explosion(self, x, y) -> None:
        """
        function that clear the current tile and add 1 pawn to the neighbours (explode)
        """
        neigbours = self.GetNeighbours(x,y) # get the neighbours of the tile

        for tile in neigbours: # for every neighbour
            try: # try to add a pawn
                if tile.SetPawns(tile.pawns+1, self.COLORS[self.player]) == False: # in case of another explosion 
                    tile.ClearPawns() # clear the tile
                    self.Explosion(tile.x,tile.y) # explode
            except RecursionError: # if not enough space to explode (too many pawns)
                self.WinMessage() # win message (last player to play wins since he overflows the board)
                return
        self.CheckPawnOwnerState() # check if the game is over or if some players are eliminated

    def ChangePlayer(self) -> None:
        """
        Change the player turn
        """
        self.player = (self.player+1) % self.PLAYER_COUNT # take the next player in the list without being out of range

        if self.player in self.eliminated_players: # if the player is eliminated (no more pawns)
            self.ChangePlayer() # we skip the player turn

        for i in self.tiles:
            for tile in i:
                tile.ChangeColor(self.COLORS[self.player]) # change the color of the tiles to the current player color

    @IsGameOver
    def ComputerPlay(self) -> None:
        """
        get every move possible in a list and then take a random one
        """
        playable_tiles = [] # list of playable tiles

        for i in self.tiles:
            for tile in i:
                if tile.owner == self.COLORS[self.player] or tile.owner == None:
                    playable_tiles.append(tile) # add the tile if playable

        if choice(playable_tiles).SetPawns(tile.pawns+1, self.COLORS[self.player]) == False: # if the tile is full
            tile.ClearPawns() # clear the tile
            self.Explosion(tile.x,tile.y) # explode
        
        self.CheckPawnOwnerState() # check if the game is over or if some players are eliminated
        self.ChangePlayer() # change the player turn
        self.SaveGameState() # save the game state

    @IsGameOver
    def CheckPawnOwnerState(self) -> None:
        """
        Check if the game is over or if some players are eliminated
        """
        #contains the owners (color) of every tile in tiles
        pawns_owner = [tile.owner for i in self.tiles for tile in i]
        count_dict = dict((i,pawns_owner.count(i)) for i in set(pawns_owner) if i is not None) # count the number of pawns for each player

        if len(count_dict) == 1: # if there is only one player left
            for key in count_dict:
                if count_dict[key] != 1: # if the only player has more than 1 pawn (meaning it's not the first round)
                    self.WinMessage()

        elif len(count_dict) < self.PLAYER_COUNT - len(self.eliminated_players): # if there is less than the number of players (some players are eliminated)
            for key in count_dict:
                if count_dict[key] != 1: # if one of the player has more than 1 pawn (meaning it's not the first rounds)
                    #loop through the colors (for the player number) and check if the color is in the count_dict if not add to eliminated_players
                    for i in range(self.PLAYER_COUNT):  
                        if self.COLORS[i] not in count_dict: # if player's pawns isn't on the board
                            if i not in self.eliminated_players: # if the player hasn't been eliminated yet
                                #show that the player has been eliminated
                                eliminated_message = tk.Message(self.window, text="Player %s (%s) has been eliminated!" % (str(i+1), self.COLORS[i]), width=200)
                                eliminated_message.pack()
                                #destroy the message after 2.5 seconds
                                self.window.after(2500, eliminated_message.destroy)
                                #add the player to the eliminated players list
                                self.eliminated_players.append(i)
                                break
        

    def WinMessage(self):
        self.game_over = True # set the game over state to true
        tk.Message(self.window, text="Player %s (%s) won!" % (str(self.player+1), self.COLORS[self.player]), width=200).pack() # show the winner
        remove("save") # delete the save file
        tk.Button(self.window, text="Quit", command=self.window.destroy).pack() # quit button
        tk.Button(self.window, text="Restart", command=lambda : (game(), self.window.destroy())).pack() # restart button
