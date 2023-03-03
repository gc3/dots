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

  def __init__(self, moves:int=20, width:int=10, height:int=10) -> None:
    self._board = [[0 for x in range(width)] for y in range(height)];
    self._score = 0;
    self._moves = moves;
    self._width = width;
    self._height = height;

    if __debug__:
      self.printBoard()

  #
  # Handle dots
  #
  def selectDot (self, y:int, x:int) -> None:
    # XXX gc3: TODO handle what happens when someone clicks on a dot and what
    #               about dragging?
    self.getDot(y, x);

  def setDot(self, y:int, x:int, color:int) -> None:
    if (self.isLocationValid(y, x)):
      self._board[y][x] = color;

    if __debug__:
      self.printBoard()

  def getDot(self, y:int, x:int) -> int:
    if (self.isLocationValid(y, x)):
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
  def getHeight(self) -> int:
    return self._height;

  def getWidth(self) -> int:
    return self._width;

  def isLocationValid(self, y:int, x:int) -> bool:
    if (y < 0 or y >= self._height):
      raise IndexError("Height out of bounds");

    if (x < 0 or x >= self._width):
      raise IndexError("Width out of bounds");

    return True;

  def printBoard(self) -> None:
    print ("Board Contents:");
    for y in range(self._height):
      row = [];
      for x in range(self._width):
        row.append(self._board[y][x]);
      print (row);
    print ("");
