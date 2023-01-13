#                         ,_     _
#                         |\\_,-~/
#                         / _  _ |    ,--.
#                        (  @  @ )   / ,-'
#                         \  _T_/-._( (
#                         /         `. \
#                        |         _  \ |
#                         \ \ ,  /      |
#                          || |-_\__   /
#                         ((_/`(____,-'
#
#                     Martin Wojtasikiewicz
from const import *
import Game
game = Game.game()
#game.PlaceTiles()
game.ChangeColor("blue")
game.GetNeighbours(0,0)
game.window.mainloop()

