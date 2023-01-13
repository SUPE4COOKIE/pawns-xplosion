import tkinter as tk
from Game.Tile import Tile


class game:
    def __init__(self, BOX_SIZE=100, TITLE="Game") -> None:
        self.BOX_SIZE = BOX_SIZE
        self.PLAYER_COUNT = 3  # self.AskPlayerCount()
        self.COLUMN, self.ROW = 3,4 # self.AskColumnRow()
        self.WIDTH = BOX_SIZE*self.COLUMN
        self.HEIGHT = BOX_SIZE*self.ROW
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT, bg="blue", highlightbackground="black")

        self.tiles = [[Tile(self.BOX_SIZE,self.canvas , self.SetCapacity(x, y),x,y,self.Explosion) for y in range(self.ROW)]
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
    
    def Explosion(self, x, y):
        #add 1 to every case around
        neigbours = self.GetNeighbours(x,y)
        for tile in neigbours:
            tile.AddPawn()

        

    def ChangeColor(self,color):
        for x in range(self.COLUMN):
            for y in range(self.ROW):
                self.tiles[x][y].PlaceTile(color)
