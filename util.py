#! /usr/bin/env python

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: utility code shared by the ui and game logic
"""

import wx

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
  DOT_YELLOW  =  3
  DOT_MAX     =  4

  def getBitmap(color: int) -> wx.Bitmap:
    """
      Turn the DotsColor constants into visible RGB tuples in order to
      set the background of this button.
    """
    path_to_png = ""
    match color:
      case DotsColor.DOT_BLUE:
        path_to_png = "images/blue.png"

      case DotsColor.DOT_GREEN:
        path_to_png = "images/green.png"

      case DotsColor.DOT_RED:
        path_to_png = "images/red.png"

      case DotsColor.DOT_YELLOW:
        path_to_png = "images/yellow.png"

      case _:
        return None # XXX gc3: FIXME should be a raise exception

    return wx.Bitmap(name=path_to_png, type=wx.BITMAP_TYPE_PNG)

