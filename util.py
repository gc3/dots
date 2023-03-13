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
    wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
    1500,
    None
  )
  wx.Yield()

def decodeMouseEvent(event:wx.MouseEvent):
  """
    Given a mouse event, decode the event type to a string so we know
    what's actually going on. Useful for debugging.
  """
  event_type = event.GetEventType()
  if event_type == wx.EVT_LEFT_DOWN._getEvtType():
      return "EVT_LEFT_DOWN"
  elif event_type ==  wx.EVT_LEFT_UP._getEvtType():
    return "wxEVT_LEFT_UP "
  elif event_type ==  wx.EVT_LEFT_DCLICK._getEvtType():
    return "wxEVT_LEFT_DCLICK"
  elif event_type ==  wx.EVT_MIDDLE_DOWN._getEvtType():
    return "wxEVT_MIDDLE_DOWN"
  elif event_type ==  wx.EVT_MIDDLE_UP._getEvtType():
    return "wxEVT_MIDDLE_UP"
  elif event_type ==  wx.EVT_MIDDLE_DCLICK._getEvtType():
    return "wxEVT_MIDDLE_DCLICK"
  elif event_type ==  wx.EVT_RIGHT_DOWN._getEvtType():
    return "wxEVT_RIGHT_DOWN"
  elif event_type ==  wx.EVT_RIGHT_UP._getEvtType():
    return "wxEVT_RIGHT_UP"
  elif event_type ==  wx.EVT_RIGHT_DCLICK._getEvtType():
    return "wxEVT_RIGHT_DCLICK"
  elif event_type ==  wx.EVT_MOUSE_AUX1_DOWN._getEvtType():
    return "wxEVT_AUX1_DOWN"
  elif event_type ==  wx.EVT_MOUSE_AUX1_UP._getEvtType():
    return "wxEVT_AUX1_UP"
  elif event_type ==  wx.EVT_MOUSE_AUX1_DCLICK._getEvtType():
    return "wxEVT_AUX1_DCLICK"
  elif event_type ==  wx.EVT_MOUSE_AUX2_DOWN._getEvtType():
    return "wxEVT_AUX2_DOWN"
  elif event_type ==  wx.EVT_MOUSE_AUX2_UP._getEvtType():
    return "wxEVT_AUX2_UP"
  elif event_type ==  wx.EVT_MOUSE_AUX2_DCLICK._getEvtType():
    return "wxEVT_AUX2_DCLICK"
  elif event_type ==  wx.EVT_MOTION._getEvtType():
    return "wxEVT_MOTION"
  elif event_type ==  wx.EVT_ENTER_WINDOW._getEvtType():
    return "wxEVT_ENTER_WINDOW"
  elif event_type ==  wx.EVT_LEAVE_WINDOW._getEvtType():
    return "wxEVT_LEAVE_WINDOW"
  elif event_type ==  wx.EVT_MOUSEWHEEL._getEvtType():
    return "wxEVT_MOUSEWHEEL"
  elif event_type ==  wx.EVT_MOUSE_EVENTS._getEvtType():
    return "all mouse events"
  elif event_type ==  wx.EVT_MAGNIFY._getEvtType():
    return "wxEVT_MAGINFY"
  else:
    return "IDK. WTF?"

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
        raise IndexError("Color(%d) given is invalid" % color)

    return wx.Bitmap(name=path_to_png, type=wx.BITMAP_TYPE_PNG)
