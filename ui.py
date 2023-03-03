#! /usr/bin/env python

"""
  Author: gc3
  Program:
  Date:
  Description: all the ui lives here for convenience as a learner project
"""

import wx
import game

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
    box.Add(self._board, 0, wx.EXPAND)

    self.CreateStatusBar() # A Statusbar in the bottom of the window
    self.createFileMenus() # Setting up the menus and menubar.
    self.SetAutoLayout(True)
    self.SetSizer(box)
    self.Layout()

  #
  # Menus and click handlers for menu items
  #
  def createFileMenus(self):
    # create a basic file menu in the menubar
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
		# A message dialog box with an OK button
    dialog = wx.MessageDialog(self, "My Dots!", "About Dots", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()

  def onQuit(self, event):
    # Someone hit the quit button!
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

    # initialize the board by adding all the button objects
    for y in range(self._game.getHeight()):
      for x in range(self._game.getWidth()):
        button = DotsDot(self._parent, self._game, y, x)
        self.Add(button, y+x, wx.EXPAND)

    self.resetBoard()

  #
  # Reset the board by applying the color changes to the ui
  #     XXX gc3: FIXME -- need to solidify a comment style for methods&classes
  def resetBoard(self):
    for y in range(self._game.getHeight()):
      for x in range(self._game.getWidth()):
        None;
        #button = self.Get(y+x) # XXX gc3: TODO set some colors yo!
        #button.changeColor()


###########################################################
#
# DotsDot
#   The the dots a board is composed of that are like items you
#   can multi-select via dragging as you play the game
#
class DotsDot(wx.Button):
  def __init__(self, parent, game:game.DotsGame, y:int, x:int):
    wx.Button.__init__(self ,parent, wx.ID_ANY, label=str(y)+", "+str(x));
    self._y = y
    self._x = x
    self._game = game
    self.Bind(wx.EVT_BUTTON, self.onClick)

  def onClick(self, event):
    if __debug__:
      print("User clicked (" + str(self._y) + ", " + str(self._x) + ")");

    self._game.selectDot(self._y, self._x);
