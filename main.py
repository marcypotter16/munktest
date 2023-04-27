from munktest.Game import Game
from munktest.ShapeCreator import ShapeCreator

g = Game()
g.state_stack.push(ShapeCreator(g))
g.game_loop()
