#! /usr/bin/env python

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: utility code shared by the ui and game logic
"""

import wx
import wx.adv

############################################################
#
# Utility Functions
#
def createSplashScreen():
  """
    Create a splash screen for the game
  """
  bitmap = wx.Bitmap('images/splash.png', wx.BITMAP_TYPE_PNG)
  wx.adv.SplashScreen(
    bitmap,
    wx.adv.SPLASH_CENTRE_ON_SCREEN|wx.adv.SPLASH_TIMEOUT,
    1500,
    None
  )
  wx.Yield()


############################################################
#
# DotsColor
#   Wrapper object for the valid colors for dots in this game
#
class DotsColor:
  # Color Constants
  DOT_INVALID = -1
  DOT_BLUE    =  0
  DOT_GREEN   =  1
  DOT_RED     =  2
  DOT_YELLOW  =  3
  DOT_MAX     =  4

  # Dot Background Colors
  BG_DEFAULT  = wx.Colour(255, 255, 255, 255)
  BG_SELECTED = wx.Colour(200, 200, 200, 255)

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
        raise IndexError("Color (" + str(color) + ") given is invalid");

    return wx.Bitmap(name=path_to_png, type=wx.BITMAP_TYPE_PNG)

