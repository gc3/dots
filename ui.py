#! /usr/bin/env python

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: all the ui lives here for convenience as a learner project
"""

import wx
import game
from util import DotsColor

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

    # Because we dont have touch events, we manually handle multi-selection, and
    # this submits the currently selected dots as a "move"
    submit = wx.Button(self, wx.ID_ANY, "Submit Selection");
    submit.Bind(wx.EVT_BUTTON, self.onSubmitSelection)
    box.AddSpacer(10)
    box.Add(submit)

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
    """
      Someone has requested a new game. Reset the game logic and
      the board that represents it afterwards
    """
    self._game.reset();
    self._board.redraw();

    if __debug__:
      print ("New game! Reset all the things");

  def onSubmitSelection(self, event):
    """
      The user is requesting to lock in their selected dots and 'make their
      move', so we will execute that move and optionally redraw the board if we
      need to fill in new dots.
    """
    if __debug__:
      print ("Selection Submitted for Evaluation!")

    if (self._game.executeSelection()):
      self._board.redraw()

  def unselectAllDots(self):
    """
      A pass through to the board so we dont break encapsulation that
      ... asks the unselects the currently selected dots.
    """
    return self._board.unselectAllDots()

  # XXX gc3 - TODO
  #   - add a score and moves left counter to the UI
  #   - add a game over pop up and have them choose 'quit' or 'play again'

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

    self.initialize();

  def initialize(self):
    """
      Initialize a blank board by adding new dots to it
    """
    for y in range(self._game.getHeight()):
      for x in range(self._game.getWidth()):
        button = DotsDot(self._parent, self._game, y, x)
        self.Add(button, y+x, wx.EXPAND)

    self.Fit(self._parent); # tell the parent window to resize to match the dots
    self.Layout();          # force the re layout of the dots

  def redraw(self):
    """
      Redraw the board appearance by getting rid of all the dots and recreating
      them using the game data that we already know. This means you should reset
      the game data BEFORE calling this.
    """
    self.Clear(True);
    self.initialize();

  def unselectAllDots(self):
    """
      Make all the dots appear to be unselected.
    """

    # skip unselecting the dots if the game has an active selection
    if (self._game.hasSelection()):
      return;

    # we 'unselect' dots by simply toggling them to change their brightness
    for item in self.GetChildren():
      item.GetWindow().SetValue(False);

############################################################
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
    self._parent = parent
    self._game = game
    self._color = game.getDotColor(y,x)

    self.SetLabel(str(self._color));
    self.SetBackgroundColour(DotsColor.getRGB(self._color))
    self.Bind(wx.EVT_TOGGLEBUTTON, self.onClick)

  def onClick(self, event):
    """
      Handle a click by adding it to the set of currently selected dots
    """
    if __debug__:
      print("User clicked (" + str(self._y) + ", " + str(self._x) + ")");

    selected = self._game.selectDot(self._y, self._x)
    if (not selected):
      # if we didnt successfully add this dot to the current selection,
      # then we ought to reset the selection in the game logic and ui, so the
      # player can try again.
      self._game.clearSelection()
      self._parent.unselectAllDots()
    else:
      # otherwise, just toggle the button to visually represent being selected
      self.SetValue(True);
