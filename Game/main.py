import tkinter as tk
from Game.Tile import Tile

class game:
    def __init__(self, BOX_SIZE=100, TITLE="Game") -> None:
        self.BOX_SIZE = BOX_SIZE
        self.COLORS = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "white"]
        self.eliminated_players = []
        self.PLAYER_COUNT = 4  # self.AskPlayerCount()
        self.player = 0
        self.COLUMN, self.ROW = 3,4 # self.AskColumnRow()
        self.WIDTH = BOX_SIZE*self.COLUMN
        self.HEIGHT = BOX_SIZE*self.ROW
        self.game_over = False
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT, bg="blue", highlightbackground="black")

        self.tiles = [[Tile(self.BOX_SIZE,self.canvas , self.SetCapacity(x, y),x,y,self.ClickListener) for y in range(self.ROW)]
                      for x in range(self.COLUMN)]
        self.window.title(TITLE)
        self.window.resizable(False, False)
        self.canvas.pack()

    def AskPlayerCount(self):
        while True:
            user_input = input(
                "Enter the number of player (between 2 and 8): ")
            num = int(user_input) if user_input.isdigit() else None
            if num and 2 <= num <= 8:
                return num
            print("Invalid input. Try again.")

    def AskColumnRow(self):
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

    def SetCapacity(self, x, y):
        # corners
        if (x == 0 and y == 0) or (x == 0 and y == self.ROW-1) or (x == self.COLUMN-1 and y == 0) or (x == self.COLUMN-1 and y == self.ROW-1):
            return 1
        # edges
        elif x == 0 or y == 0 or x == self.COLUMN-1 or y == self.ROW-1:
            return 2
        # anything else
        return 3
    
    def IsGameOver(func):
        def wrapper(self, *args, **kwargs):
            if not self.game_over:
                return func(self, *args, **kwargs)
        return wrapper
    
    def IsTileOwner(func):
        def wrapper(self,*args,**kwargs):
            if self.tiles[args[0]][args[1]].owner == None or self.tiles[args[0]][args[1]].owner == self.COLORS[self.player]:
                return func(self,*args,**kwargs)
        return wrapper

    
    def GetNeighbours(self, x, y):
        #return direct neighbours (no border)
        neighbours = []
        if x > 0:
            neighbours.append(self.tiles[x-1][y])
        if x < self.COLUMN-1:
            neighbours.append(self.tiles[x+1][y])
        if y > 0:
            neighbours.append(self.tiles[x][y-1])
        if y < self.ROW-1:
            neighbours.append(self.tiles[x][y+1])
        return neighbours

    @IsTileOwner
    @IsGameOver
    def ClickListener(self, x,y):
        tile = self.tiles[x][y]
        if tile.SetPawns(tile.pawns+1, self.COLORS[self.player]) == False:
            tile.ClearPawns()
            self.Explosion(x,y)
        self.CheckPawnOwnerState()
        self.ChangePlayer()
    
    def Explosion(self, x, y):
        #add 1 to every case around
        neigbours = self.GetNeighbours(x,y)
        for tile in neigbours:
            try:
                if tile.SetPawns(tile.pawns+1, self.COLORS[self.player]) == False: # in case of another explosion 
                    tile.ClearPawns()
                    self.Explosion(tile.x,tile.y)
            except RecursionError: # caused by not enough space to explode (too many pawns)
                pass
        #self.CheckPawnOwnerState()

    def ChangePlayer(self):
        self.player = (self.player+1) % self.PLAYER_COUNT
        if self.player in self.eliminated_players:
            self.ChangePlayer()
        for i in self.tiles:
            for tile in i:
                tile.ChangeColor(self.COLORS[self.player])

    def CheckPawnOwnerState(self):
        #contains the attributes of every tile in tiles
        pawns_owner = [tile.owner for i in self.tiles for tile in i]
        count_dict = dict((i,pawns_owner.count(i)) for i in set(pawns_owner) if i is not None)
        print(count_dict)
        if len(count_dict) == 1:
            for key in count_dict:
                if count_dict[key] != 1: # if the only player has more than 1 pawn (meaning it's not the first rounds)
                    self.WinMessage()
        elif len(count_dict) < self.PLAYER_COUNT:
            for key in count_dict:
                if count_dict[key] != 1: # if one of the player has more than 1 pawn (meaning it's not the first rounds)
                    #loop through the colors (for the player number) and check if the color is in the count_dict if not add to eliminated_players
                    for i in range(self.PLAYER_COUNT):
                        if self.COLORS[i] not in count_dict:
                            if i not in self.eliminated_players:
                                print("Player", self.COLORS[i], "has been eliminated")
                                eliminated_message = tk.Message(self.window, text="Player %s (%s) has been eliminated!" % (str(i+1), self.COLORS[i]), width=200)
                                eliminated_message.pack()
                                self.window.after(2500, eliminated_message.destroy)
                                self.eliminated_players.append(i)
                                break
        

    def WinMessage(self):
        self.game_over = True
        tk.Message(self.window, text="Player %s (%s) won!" % (str(self.player+1), self.COLORS[self.player]), width=200).pack()
        tk.Button(self.window, text="Quit", command=self.window.destroy).pack()
