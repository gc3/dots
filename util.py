#! /usr/bin/env python

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: utility code shared by the ui and game logic
"""


############################################################
#
# DotsColor
#   Wrapper object for the valid colors for dots in this game
#
class DotsColor:
  DOT_INVALID = -1
  DOT_BLUE    =  0
  DOT_GREEN   =  1
  DOT_RED     =  2
  DOT_MAX     =  3

  def getRGB(color: int) -> tuple:
    """
      Turn the DotsColor constants into visible RGB tuples in order to
      set the background of this button.
    """
    match color:
      case DotsColor.DOT_BLUE:
        return (0, 100, 255, 255)

      case DotsColor.DOT_GREEN:
        return (0, 200, 0, 255)

      case DotsColor.DOT_RED:
        return (200, 0, 0, 255)

      case _:
        return (0, 0, 0, 0)


