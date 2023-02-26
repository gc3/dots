#! /usr/bin/env python

"""
  Author: gc3
  Program:
  Date:
  Description: game logic lives here
"""

class DotsGame():
  # XXX gc3: FIXME -- doc blocks?

  DOT_EMPTY = 0
  DOT_BLUE  = 1
  DOT_GREEN = 2
  DOT_RED   = 3

  # XXX gc3: what does this need to know to run the game?
  def __init__(self, moves:int=20, width:int=10, height:int=10):
    self._board = [[0 for x in range(width)] for y in range(height)];
    self._score = 0;
    self._moves = moves;

    print("XXX gc3: game logic constructor")
    print(self._board);

  def selectDot (self, y:int, x:int):
    # XXX gc3: TODO handle what happens when someone clicks on a dot
    self.getDot(y, x);

  def setDot(self, y:int, x:int, color:int):
    self._board[y][x] = color;
    print (self._board);

  def getDot(self, y:int, x:int) -> int:
    print (self._board[y][x]);
    return self._board[y][x];

  def getScore(self) -> int:
    return self._score;

  def isGameOver(self) -> bool:
    return (self._moves == 0);
