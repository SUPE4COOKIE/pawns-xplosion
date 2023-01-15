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
#           Martin Wojtasikiewicz - Yanis Kherouni
import Game
if __name__ == "__main__":
    game = Game.game() # create an instance of the game
    game.LoadGameState() # load the game state (if there is one)
    game.window.mainloop()

