#! /usr/bin/env python

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: game logic lives here
"""
import random
from util import DotsColor

############################################################
#
# DotsGame
#   The interface to the game logic for Dots. The UI goes
#   here to get anything done inside the game.
#
class DotsGame():
  def __init__(self, max_moves:int=20, height:int=10, width:int=10) -> None:
    self._width = width;
    self._height = height;
    self._moves_max = max_moves;
    self._board = DotsGameBoard(height, width)

    self.reset()

  ###
  # Game Management
  #
  def reset(self) -> None:
    """
      Reset the game by re-initializing all of the player interacting data
    """
    self._moves_left = self._moves_max;
    self._score = 0;
    self._current_selection = [];
    self._board.initialize();

  def isGameOver(self) -> bool:
    """
      Is the game over? It is when there's no more moves left
    """
    return (self._moves_left <= 0);

  ###
  # Accessors
  #
  def getScore(self) -> int:
    """
      Get the current game score which is the number of dots removed by the
      player so far
    """
    return self._score;

  def getHeight(self) -> int:
    """
      The vertical size of the game board in number of dots (number of rows)
    """
    return self._height;

  def getWidth(self) -> int:
    """
      The horizontal size of the game board in number of dots (number of cols)
    """
    return self._width;


  def getDotColor(self, y:int, x:int) -> int:
    """
      A pass through to the game board that gets the color of the dot
      at location (y,x)
    """
    return self._board.getDotColor(y, x);

  ###
  # Dot Selection Logic
  #
  def hasSelection(self) -> bool:
    """
      Return True iff any dots are selected
    """
    return (len(self._current_selection) != 0)

  def clearSelection(self) -> None:
    """
      Remove all dots from the current selection
    """
    self._current_selection.clear()

  def selectDot(self, y:int, x:int) -> bool:
    """
      Given (y, x) coordinates, add the dot at that position in the board
      to the current selection
    """
    if (not self._board.isLocationValid(y, x)):
      return;

    # XXX gc3: FIXME -- using tuples for a dot here is kinda sketchy
    selected_dot = (y, x, self._board.getDotColor(y, x))

    # starting a new selection, so add the first dot
    if (not self._current_selection):
      self._current_selection.append(selected_dot);

    # if we have a selection going, reset it if
    #   - is already in the selection set
    #   - is not adjascent to an existing dot in the selection
    #   - is a different color than all the existing dots in the selection
    elif (selected_dot in self._current_selection or
          False or # XXX gc3: TODO check adjascency
          self._current_selection[0][2] != selected_dot[2]):
      return False;

    # otherwise add this dot to the current set of selected dots
    else:
      self._current_selection.append(selected_dot);

    return True;

  def executeSelection(self) -> bool:
    """
      Take the current selection and 'execute' it for the player, which will
      remove the correct dots, replace them with new ones, and adjust the
      score/moves to help the game progress.

      NB: This method *assumes* that the selection is valid because selectDot()
          will only allow valid dots to be added or fail.
    """
    if __debug__:
      print (self._current_selection);

    # without a selection, there's nothing to do
    if (not self.hasSelection()):
      return False

    # 'Remove' the current selection by
    #   1. copying the colors of the dots 'above' the selection in each column
    #      into the spaces currently occupied by the selection.
    #   2. marking dots that were copied as DOT_INVALID
    #   3. fill in the dots marked with new colors

    # grab the highest and lowest row from the selection in each column of the
    # selection, so we know which dots to move down and how many spaces to move
    # them XXX gc3: FIXME -- this version doesnt work yet, but i'm sleepy
    affected_cols = [self._width] * self._width
    for dot in self._current_selection:
      if (dot[0] < affected_cols[dot[1]]):
        affected_cols[dot[1]] = dot[0]

    print(affected_cols)

    self._board.fillEmptyDots()

    # make sure the player gets credit for their selection
    self._score += len(self._current_selection);
    self._moves_left -= 1;

    # we are done, so clear the selection for the player to go again
    self.clearSelection()
    return True

############################################################
#
# DotsGameBoard
#   Handle the board (a 2d array) and its contained dots (a
#   color at a location in the board)
#
class DotsGameBoard():
  def __init__(self, height:int=10, width:int=10) -> None:
    self._height = height
    self._width = width
    self._board = []

  def initialize(self) -> None:
    """
      We initialize a board by assigning every slot in it a random
      color within the DotsColor set.
    """
    self._board = [
      [random.randrange(DotsColor.DOT_MAX) for x in range(self._width)]
      for y in range(self._height)
    ]

    if __debug__:
      self.print()

  def fillEmptyDots(self) -> None:
    """
      Find all of the "empty" dots in the board and fill them with a new,
      random color. This is useful after removing dots because of a successful
      selection by the player.
    """
    for y in range(self._height):
      for x in range(self._width):
        if (self.getDotColor(y, x) == DotsColor.DOT_INVALID):
          self_board[y][x] = random.randrange(DotsColor.DOT_MAX)

  def getDotColor(self, y:int, x:int) -> int:
    """
      Return the color (from DotsColor) at (y,x) in this board
    """
    if (self.isLocationValid(y, x)):
      return self._board[y][x];
    else:
      return DotsColor.DOT_INVALID;

  def isLocationValid(self, y:int, x:int) -> bool:
    """
      Test if the given (y, x) coordinates are valid for this board
    """
    if (y < 0 or y >= self._height):
      raise IndexError("Height out of bounds");

    if (x < 0 or x >= self._width):
      raise IndexError("Width out of bounds");

    return True;

  def print(self) -> None:
    """
      A utility helper that prints out this board's contents
    """
    print ("Board Contents:");

    for y in range(self._height):
      row = [];
      for x in range(self._width):
        row.append(self._board[y][x]);
      print (row);

    print ("");


