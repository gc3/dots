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

  MOVE_ACCEPTED  = 0
  MOVE_REJECTED  = 1
  MOVE_ENDS_GAME = 2

  def __init__(self, max_moves:int=20):
    self._width = 10
    self._height = 10
    self._moves_max = max_moves
    self._board = DotsGameBoard(self._height, self._width)

    self.reset()

  ###
  # Game Management
  #
  def reset(self) -> None:
    """
      Reset the game by re-initializing all of the player interacting data
    """
    self._moves_left = self._moves_max
    self._score = 0
    self._current_selection = []
    self._board.initialize()

  def isGameOver(self) -> bool:
    """
      Is the game over? It is when there's no more moves left
    """
    return (self._moves_left <= 0)

  ###
  # Accessors
  #
  def getScore(self) -> int:
    """
      Get the current game score which is the number of dots removed by the
      player so far
    """
    return self._score

  def getMovesLeft(self) -> int:
    """
      Get how many moves are left until the game is over
    """
    return self._moves_left

  def getHeight(self) -> int:
    """
      The vertical size of the game board in number of dots (number of rows)
    """
    return self._height

  def getWidth(self) -> int:
    """
      The horizontal size of the game board in number of dots (number of cols)
    """
    return self._width


  def getDotColor(self, y:int, x:int) -> int:
    """
      A pass through to the game board that gets the color of the dot
      at location (y,x)
    """
    return self._board.getDotColor(y, x)

  ###
  # Dot Selection Logic / Move Execution
  #
  def hasSelection(self) -> bool:
    """
      Return True iff any dots are selected
    """
    return (len(self._current_selection) != 0)

  def isSelected(self, y:int, x:int) -> bool:
    """
      Return True iff the given coordinates identify a dot in the current
      set of selected dots being tracked
    """
    tmp = DotsGameDot(y, x, -1)
    return tmp in self._current_selection

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
      return False

    selected_dot = DotsGameDot(y, x, self._board.getDotColor(y, x))

    # starting a new selection, so add the first dot
    if (not self._current_selection):
      self._current_selection.append(selected_dot)

    # if we have already seen this dot, ignore it
    elif (selected_dot in self._current_selection):
      pass

    # if we have a selection going, reset it if
    #   - is a different color than all the existing dots in the selection
    #   - is not adjascent to an existing dot in the selection
    elif ((self._current_selection[0].color != selected_dot.color) or
          not self._board.isAdjascent(selected_dot, self._current_selection)):
      return False

    # otherwise add this dot to the current set of selected dots
    else:
      self._current_selection.append(selected_dot)

    return True

  def executeSelection(self) -> int:
    """
      Take the current selection and 'execute' it for the player, which will
      remove the correct dots, replace them with new ones, and adjust the
      score/moves to help the game progress.

      NB: This method *assumes* that the selection is valid because selectDot()
          will only allow valid dots to be added or fail.
    """
    if __debug__:
      print ("Selection Execute! {")
      for dot in self._current_selection:
        print ("  " + str(dot))
      print ("}")

    # without a selection, there's nothing to do
    if (not self.hasSelection()):
      return self.MOVE_REJECTED

    # if we only have 1 dot selected, we dont do anything. this fixes both
    # single click issues and enforces a rule that you have to have at least 2
    # dots connected to make a proper selection which feels right
    if (len(self._current_selection) == 1):
      return self.MOVE_REJECTED

    # 'Remove' the current selection by
    #   1. grabbing the highest and lowest row from the selection in each column
    #      of the selection, so we know which dots to move down and how many
    #      spaces to move
    affected_bottoms = [-1] * self._width
    affected_tops = [self._width] * self._width
    for dot in self._current_selection:
      if (dot.y > affected_bottoms[dot.x]):
        affected_bottoms[dot.x] = dot.y

      if (dot.y < affected_tops[dot.x]):
        affected_tops[dot.x] = dot.y

    #   2. for each column that is affected by this selection, asking the board
    #      to use that data to shift the column down
    for i in range(self._width):
      if (affected_bottoms[i] != -1):
        self._board.moveDotsDown(i, affected_tops[i], affected_bottoms[i])

    # make sure the player gets credit for their selection
    self._score += len(self._current_selection)
    self._moves_left -= 1

    if __debug__:
      self._board.print()

    # move is executed, so clear the selection for the player to go again or
    # end the game there are no moves left
    self.clearSelection()
    return self.MOVE_ENDS_GAME if self.isGameOver() else self.MOVE_ACCEPTED

############################################################
#
# DotsGameBoard
#   Handle the board (a 2d array) and its contained dots (a
#   color at a location in the board)
#
class DotsGameBoard():
  def __init__(self, height:int, width:int):
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

  def moveDotsDown(self, col:int, top:int, bottom:int) -> None:
    """
      Given the top and bottom coordinate for the given column, col, move
      the dots above top in col down to bottom and replace the newly empty
      dots with new colors
    """
    # save the original dot colors so we can overwrite them later
    col_dots = []
    for y in range(self._height):
      col_dots.append(self._board[y][col])

    # move the dots down by 'shift' rows
    shift = 1 + (bottom - top)
    for y in range(self._height):
      if (y < shift):
        # recreate new dots for row entries at the top of this colum because we
        # are filling 'down'
        self._board[y][col] = random.randrange(DotsColor.DOT_MAX)

      if (y < top):
        # shift the dots down that are above the dots being removed
        self._board[y + shift][col] = col_dots[y]

  def getDotColor(self, y:int, x:int) -> int:
    """
      Return the color (from DotsColor) at (y,x) in this board
    """
    return (
      self._board[y][x] if self.isLocationValid(y, x) else DotsColor.DOT_INVALID
    )

  def isLocationValid(self, y:int, x:int) -> bool:
    """
      Test if the given (y, x) coordinates are valid for this board
    """
    if (y < 0 or y >= self._height):
      raise IndexError("Height out of bounds")

    if (x < 0 or x >= self._width):
      raise IndexError("Width out of bounds")

    return True

  def isAdjascent(self, dot, selection) -> bool:
    """
      Given a dot and selection of dots (list), return true if the dot
      is "adjascent" to at least one of the dots in the selection.
    """
    for item in selection:
      y_delta = abs(dot.y - item.y)
      x_delta = abs(dot.x - item.x)
      if ((y_delta == 0 and x_delta == 1) or
          (y_delta == 1 and x_delta == 0)):
        return True

    return False

  def print(self) -> None:
    """
      A utility helper that prints out this board's contents
    """
    print ("Board Contents:")

    for y in range(self._height):
      row = []
      for x in range(self._width):
        row.append(self._board[y][x])
      print (row)

    print ("")

############################################################
#
# DotsGameDot
#   A quick struct to wrap the (y, x) coordinates of a dot &
#   its color
#
class DotsGameDot():
  def __init__(self, y: int, x:int, color:int):
    self.y = y
    self.x = x
    self.color = color

  def __eq__(self, other):
    return (
      (self.y == other.y) and
      (self.x == other.x)
    )

  def __str__(self, ) -> str:
    return "Dot(%d, %d, %d)" % (self.y, self.x, self.color)
