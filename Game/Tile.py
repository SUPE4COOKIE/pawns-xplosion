class Tile:
    def __init__(self, BOX_SIZE, canvas, capacity, x, y,explosion) -> None:
        self.BOX_SIZE : int = BOX_SIZE + 2 # 2 is the size of the outline
        self.pawns: int = 0
        self.owner: int = 0
        self.capacity: int = capacity
        self.canvas = canvas
        self.x = x
        self.y = y
        self.Explosion = explosion
        self.PlaceTile()
    
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

    def AddPawn(self, color):
        print("Clicked on tile at", self.x, self.y)

        if self.pawns < self.capacity:
            if self.pawns == 0:
                self.centerpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/8, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/8, self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/8, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/8, fill=color)
            elif self.pawns == 1:
                self.ClearPawns()
                self.leftpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/3, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/3, self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/10, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/10, fill=color)
                self.rightpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/10, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/10, self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/3, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/3, fill=color)
            elif self.pawns == 2:
                self.centerpawn = self.canvas.create_oval(self.x*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/8, self.y*self.BOX_SIZE + self.BOX_SIZE/2 - self.BOX_SIZE/8, self.x*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/8, self.y*self.BOX_SIZE + self.BOX_SIZE/2 + self.BOX_SIZE/8, fill=color)
            self.pawns += 1
        else:
            self.ClearPawns()
            print("Tile is full")
            self.pawns = 0

    def PlaceTile(self,color="red"):
        try:
            self.canvas.delete(self.rectangle)
        except AttributeError:
            pass
        
        self.rectangle = self.canvas.create_rectangle(
            self.x*self.BOX_SIZE, self.y*self.BOX_SIZE, (self.x+1)*self.BOX_SIZE, (self.y+1)*self.BOX_SIZE, fill="black", outline=color, width=2)
            
        self.canvas.tag_bind(self.rectangle, "<Button-1>", lambda _ : self.AddPawn(color))
