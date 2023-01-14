class Tile:
    def __init__(self, BOX_SIZE, canvas, capacity, x, y,clicklistener) -> None:
        self.BOX_SIZE : int = BOX_SIZE + 2 # 2 is the size of the outline
        self.pawns: int = 0
        self.owner: str = None
        self.capacity: int = capacity
        self.canvas = canvas
        self.x = x
        self.y = y
        self.ClickListener = clicklistener
        self.__PlaceTile()
    
    def ClearPawns(self):
        if self.pawns == 1:
            self.canvas.delete(self.centerpawn)
        elif self.pawns == 2:
            self.canvas.delete(self.leftpawn)
            self.canvas.delete(self.rightpawn)
        elif self.pawns >= 3:
            self.canvas.delete(self.centerpawn)
            self.canvas.delete(self.leftpawn)
            self.canvas.delete(self.rightpawn)
        self.pawns = 0
        self.owner = None

    def CapacityCheck(func):
        def wrapper(self,*args,**kwargs):
            if self.pawns < self.capacity:
                return func(self,*args,**kwargs)
            else:
                return False
        return wrapper
    
    @CapacityCheck
    def SetPawns(self,pawns,color):
        self.ClearPawns()
        self.pawns = pawns
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
            
        self.owner = color

    def ChangeColor(self, color):
        self.canvas.itemconfig(self.rectangle, outline=color)
    
    def __PlaceTile(self,color="red"):
        self.rectangle = self.canvas.create_rectangle(
            self.x*self.BOX_SIZE, self.y*self.BOX_SIZE, (self.x+1)*self.BOX_SIZE, (self.y+1)*self.BOX_SIZE, fill="black", outline=color, width=2)
        
        self.canvas.tag_bind(self.rectangle, "<Button-1>", lambda _ : self.ClickListener(self.x, self.y))
    
