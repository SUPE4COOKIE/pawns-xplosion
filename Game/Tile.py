class Tile:
    def __init__(self, BOX_SIZE, canvas, capacity, x, y,clicklistener) -> None:
        self.BOX_SIZE : int = BOX_SIZE + 2 # 2 is the size of the outline
        self.pawns: int = 0 # number of pawns on the tile
        self.owner: str = None # color of the owner
        self.capacity: int = capacity # max number of pawns on the tile
        self.canvas = canvas # canvas to draw on
        self.x = x # x coordinate of the tile in the grid
        self.y = y # y coordinate of the tile in the grid
        self.ClickListener = clicklistener # function to call when the tile is clicked
        self.__PlaceTile() # draw the tile
    
    def ClearPawns(self) -> None:
        """
        clears the pawns on the tile
        """
        # delete the pawns on the tile based on the number of pawns
        if self.pawns == 1:
            self.canvas.delete(self.centerpawn)
        elif self.pawns == 2:
            self.canvas.delete(self.leftpawn)
            self.canvas.delete(self.rightpawn)
        elif self.pawns >= 3:
            self.canvas.delete(self.centerpawn)
            self.canvas.delete(self.leftpawn)
            self.canvas.delete(self.rightpawn)
        self.pawns = 0 # set the number of pawns to 0
        self.owner = None # set the owner to None

    def CapacityCheck(func):
        """
        decorator to check if the tile is full if so return false
        """
        def wrapper(self,*args,**kwargs):
            if self.pawns < self.capacity:
                return func(self,*args,**kwargs)
            else:
                return False
        return wrapper
    
    @CapacityCheck
    def SetPawns(self,pawns,color) -> None:
        self.ClearPawns() # reset the pawns
        self.pawns = pawns # set the number of pawns to the given number

        # add the number of pawns to the tile with given color
        # The pawns size and placement is reponsive so if the size of the box change the pawns will be displayed correctly
        # The pawns are also binded to the click event so when the user clicks on the pawn the tile will be clicked
        if self.pawns == 1:
            self.centerpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/8, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/8, self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/8, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/8, fill=color)
            self.canvas.tag_bind(self.centerpawn, "<Button-1>", lambda _ : self.ClickListener(self.x, self.y))
        elif self.pawns == 2:
            self.leftpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/3, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/3, self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/10, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/10, fill=color)
            self.rightpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/10, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/10, self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/3, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/3, fill=color)
            self.canvas.tag_bind(self.leftpawn, "<Button-1>", lambda _ : self.ClickListener(self.x, self.y))
            self.canvas.tag_bind(self.rightpawn, "<Button-1>", lambda _ : self.ClickListener(self.x, self.y))
        elif self.pawns == 3:
            self.centerpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/8, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/8, self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/8, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/8, fill=color)
            self.leftpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/3, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/3, self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/10, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/10, fill=color)
            self.rightpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/10, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/10, self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/3, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/3, fill=color)
            self.canvas.tag_bind(self.centerpawn, "<Button-1>", lambda _ : self.ClickListener(self.x, self.y))
            self.canvas.tag_bind(self.leftpawn, "<Button-1>", lambda _ : self.ClickListener(self.x, self.y))
            self.canvas.tag_bind(self.rightpawn, "<Button-1>", lambda _ : self.ClickListener(self.x, self.y))
            
        self.owner = color # set the owner to the given color

    def ChangeColor(self, color) -> None:
        """
        change outline color of the tile
        """
        self.canvas.itemconfig(self.rectangle, outline=color)
    
    def __PlaceTile(self,color="red") -> None:
        """
        draw the tile on the canvas
        """
        self.rectangle = self.canvas.create_rectangle(
            self.x*self.BOX_SIZE, self.y*self.BOX_SIZE, (self.x+1)*self.BOX_SIZE, (self.y+1)*self.BOX_SIZE, fill="black", outline=color, width=2)
        
        self.canvas.tag_bind(self.rectangle, "<Button-1>", lambda _ : self.ClickListener(self.x, self.y))
    
