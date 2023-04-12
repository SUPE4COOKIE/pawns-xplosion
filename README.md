# Pawns-Xplosion

In a game played by 2 to 8 players on a rectangular board with 8 rows and 5 columns, each player has pieces of a unique color. Players take turns placing a piece either on an empty cell or a cell already containing their pieces.

Corner cells have a maximum capacity of 2 pieces, edge cells (not in corners) have a maximum capacity of 3 pieces, and inner cells have a maximum capacity of 4 pieces.

When the number of pieces in a cell reaches its maximum capacity, the pieces are distributed to adjacent cells and the original cell becomes empty. If adjacent cells contain the player's pieces, the new piece is added to them. If adjacent cells contain opponent's pieces, they are captured, change color, and the new piece is added.

After such a move, adjacent cells may have more pieces than before and could reach their maximum capacity. If so, the process repeats, potentially causing a chain reaction.
### setup

------------
#### Clone the repo

`git clone https://github.com/SUPE4COOKIE/pawns-xplosion.git`


------------



#### windows & OSX
`pip install -r requirements.txt`
`python main.py`

#### linux

`pip3 install -r requirements.txt`
`python3 main.py`

![](https://cdn.discordapp.com/attachments/931624866367565856/1064008786395807754/image.png)
