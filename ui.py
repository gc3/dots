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
    board = DotsBoard(self, game)
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(board.getBoard(), 3, wx.EXPAND)

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
    self.Close(True)

  def onNewGame(self, event):
    # XXX gc3: FIXME  create a new game of some kind. reset scores and re-init
    #                 the board, ... is this the same thing as should happen on
    #                 startup? probably
    print ("XXX gc3: new game requested!");


###########################################################
#
# DotsBoard
#   The the dots board with dots in it you can click on
#
#   XXX gc3: FIXME should this actually *be* a kind of panel / box instead of
#                  contain one? is a or has a? probably is a since i can get rid
#                  of the parent stuff when i'm beyond the testing buttons
#                  phase
#
class DotsBoard():
  def __init__(self, parent, game):
    self._parent = parent
    self._game = game

    self._box = wx.BoxSizer(wx.VERTICAL)
    button = wx.Button(self._parent, wx.ID_ANY, "Select a Blue")
    button.Bind(wx.EVT_BUTTON, self.onClick)

    button2 = wx.Button(self._parent, wx.ID_ANY, "Select a Red")
    button2.Bind(wx.EVT_BUTTON, self.onClick2)

    self._box.Add(button, 1, wx.EXPAND)
    self._box.Add(button2, 2, wx.EXPAND)

  def getBoard(self):
    return self._box;

  def onClick(self, event):
    print("XXX gc3: clicked 1")
    print(event)
    self._game.setDot(1, 1, game.DotsGame.DOT_BLUE);
    self._game.selectDot(1, 1);

  def onClick2(self, event):
    print("XXX gc3: clicked 2")
    print(event)
    self._game.setDot(0, 0, game.DotsGame.DOT_RED);
    self._game.selectDot(0, 0);

###########################################################
#
# DotsDot
#   The the dots a board is composed of that are like items you
#   can multi-select via dragging as you play the game
#
class DotsDot():
  def __init__(self):
    print("XXX gc3: dot constructor")
