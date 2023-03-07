#! /usr/bin/env python

"""
  Author: gc3
  Program:
  Date:
  Description: game logic lives here
"""
import random

class DotsGame():
  def __init__(self, max_moves:int=20, height:int=10, width:int=10) -> None:
    self._width = width;
    self._height = height;
    self._moves_max = max_moves;

    self.resetGame()

  #
  # Handle dots
  #   XXX gc3: FIXME -- using tuples for a dot here is kinda sketchy
  #       need to make a board and a dot class ....
  #
  def resetGame(self) -> None:
    self._moves_curr = 0;
    self._score = 0;
    self._currentSelection = [];
    self.initializeBoard();

  def initializeBoard(self) -> None:
    self._board = [
      [random.randrange(DotsColor.DOT_MAX) for x in range(self._width)]
      for y in range(self._height)
    ]

    if __debug__:
      self.printBoard()

  def selectDot(self, y:int, x:int) -> bool:
    if (not self.isLocationValid(y, x)):
      return;

    new_dot = (y, x, self.getDot(y, x))

    # starting a new selection, so add the first dot
    if (not self._currentSelection):
      self._currentSelection.append(new_dot);

    # if we have a selection going, reset it if
    #   - is already in the selection set
    #   - is not adjascent to an existing dot in the selection
    #   - is a different color than all the existing dots in the selection
    elif (new_dot in self._currentSelection or
          False or # XXX gc3: TODO check adjascency
          self._currentSelection[0][2] != new_dot[2]): # XXX gc3: FIXME janky AF
      self._currentSelection.clear()
      return False;

    # otherwise add this dot to the current set of selected dots
    else:
      self._currentSelection.append(new_dot);

    print (self._currentSelection); # XXX gc3; FIXME -- kill this
    return True;

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
   return (self._moves_curr == 0);

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

class DotsColor:
  DOT_BLUE  =  0
  DOT_GREEN =  1
  DOT_RED   =  2
  DOT_MAX   =  3

  def __init__(self, color:int) -> None:
    self._color = color
