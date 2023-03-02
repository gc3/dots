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

  def __init__(self, moves:int=20, width:int=10, height:int=10):
    self._board = [[0 for x in range(width)] for y in range(height)];
    self._score = 0;
    self._moves = moves;
    self._width = width;
    self._height = height;

    print("XXX gc3: game logic constructor")
    print(self._board);

  #
  # Handle dots
  #
  def selectDot (self, y:int, x:int):
    # XXX gc3: TODO handle what happens when someone clicks on a dot and what
    #               about dragging?
    self.getDot(y, x);

  def setDot(self, y:int, x:int, color:int):
    if (self.isXYValid(y, x)):
      self._board[y][x] = color;
      print (self._board);

  def getDot(self, y:int, x:int) -> int:
    if (self.isXYValid(y, x)):
      return self._board[y][x];
  #
  # Handle scoring
  #
  def getScore(self) -> int:
    return self._score;

  #
  # Handle moves / game status
  #
  def isGameOver(self) -> bool:
   return (self._moves == 0);

  #
  # Utilites
  #
  def isXYValid(self, y:int, x:int):
    if (y < 0 or y >= self._height):
      raise IndexError("Height out of bounds");

    if (x < 0 or x >= self._width):
      raise IndexError("Width out of bounds");

    return True;
