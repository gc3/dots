#! /usr/bin/env python

"""
  Author: gc3
  Program:
  Date:
  Description: all the ui lives here for convenience as a learner project
"""

import wx
import game
from game import DotsColor

###########################################################
#
# Dots Frame
#   The main frame for a dots game that contains the board
#
class DotsFrame(wx.Frame):
  def __init__(self, parent, ID, title, game):
    wx.Frame.__init__(self, parent, ID, title, size=(800, 800))

    self._game = game;

		# Setting up the dots board in a simple layout
    self._board = DotsBoard(self, self._game)
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(self._board, wx.SHAPED)

    self.CreateStatusBar() # A Statusbar in the bottom of the window
    self.createFileMenus() # Setting up the menus and menubar.
    self.SetAutoLayout(True)
    self.SetSizer(box)
    self.Layout()

  def createFileMenus(self):
    """
      create a basic file menu in the menubar
    """
    filemenu = wx.Menu()
    menuitem = filemenu.Append(wx.ID_ANY, "About", "About this Program")
    self.Bind(wx.EVT_MENU, self.onAbout, menuitem)

    filemenu.AppendSeparator()

    menuitem = filemenu.Append(wx.ID_ANY, "New Game", "Start a new game")
    self.Bind(wx.EVT_MENU, self.onNewGame, menuitem)

    filemenu.AppendSeparator()

    menuitem = filemenu.Append(wx.ID_ANY, "Quit", "Quit, mang!")
    self.Bind(wx.EVT_MENU, self.onQuit, menuitem)

    menubar = wx.MenuBar()
    menubar.Append(filemenu,"File")
    self.SetMenuBar(menubar)

  def onAbout(self,  event):
    """
		  A message dialog box with an OK button
    """
    dialog = wx.MessageDialog(self, "My Dots!", "About Dots", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()

  def onQuit(self, event):
    """
      Someone hit the quit button!
    """
    if __debug__:
      print ("Someone hit the quit button!");
    self.Close(True)

  def onNewGame(self, event):
    self._game.resetGame();
    self._board.resetBoard();

    if __debug__:
      print ("New game! Reset all the things");


###########################################################
#
# DotsBoard
#   The the dots board with dots in it you can click on
#
class DotsBoard(wx.GridSizer):
  def __init__(self, parent, game:game.DotsGame):
    wx.GridSizer.__init__(self, game.getWidth(), game.getHeight(), 5, 5)

    self._game = game
    self._parent = parent

    self.initializeBoard();

  def initializeBoard(self):
    """
      Initialize a blank board by adding new dots to it
    """
    for y in range(self._game.getHeight()):
      for x in range(self._game.getWidth()):
        button = DotsDot(self._parent, self._game, y, x)
        self.Add(button, y+x, wx.EXPAND)

    self.Fit(self._parent); # tell the parent window to resize to match the dots
    self.Layout();          # force the re layout of the dots

  def resetBoard(self):
    """
      Reset the board getting rid of all the dots and recreating them using the
      game data that we already know. This means you should reset the game data
      BEFORE calling this.
    """
    self.Clear(True);
    self.initializeBoard();



###########################################################
#
# DotsDot
#   The the dots a board is composed of that are like items you
#   can multi-select via dragging as you play the game
#
class DotsDot(wx.ToggleButton):
  def __init__(self, parent, game:game.DotsGame, y:int, x:int):
    wx.Button.__init__(self, parent, wx.ID_ANY);

    self._y = y
    self._x = x
    self._game = game
    self._color = game.getDot(y,x)

    self.SetLabel(str(self._color));
    self.SetBackgroundColour(self.getRGB())
    self.Bind(wx.EVT_TOGGLEBUTTON, self.onClick)

  def getRGB(self):
    match self._color:
      case DotsColor.DOT_BLUE:
        return (0, 100, 255, 255)

      case DotsColor.DOT_GREEN:
        return (0, 200, 0, 255)

      case DotsColor.DOT_RED:
        return (200, 0, 0, 255)

      case _:
        return (0, 0, 0, 0)

  def onClick(self, event):
    """
      Handle a click by adding it to the set of currently selected dots
    """
    if __debug__:
      print("User clicked (" + str(self._y) + ", " + str(self._x) + ")");

    selected = self._game.selectDot(self._y, self._x);
    if (not selected):
      # XXX gc3: FIXME in this case we have to undo all the selected dots >.<
      print ("XXX gc3: figure out hwo to undo all the selected dots, yo");
    else:
      self.SetValue(True);
