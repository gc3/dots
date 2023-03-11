#! /usr/bin/env python

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: all the ui lives here for convenience as a learner project
"""

import game
from util import DotsColor
import wx

###########################################################
#
# Dots Frame
#   The main frame for a dots game that contains the board
#
class DotsFrame(wx.Frame):

  # Some default colors to be reused
  BG_GREY   = wx.Colour(50, 50, 50, 255)
  BG_WHITE  = wx.Colour(255, 255, 255, 255)

  def __init__(self, parent, ID, title, game):
    wx.Frame.__init__(self, parent, ID, title)

    self._game = game;

    # Setting up the menus and menubar.
    self.createFileMenus()

		# Setting up the dots board in a simple layout
    box = wx.BoxSizer(wx.VERTICAL)

    self._board = DotsBoard(self, self._game)
    box.Add(self._board, flag=wx.ALL|wx.EXPAND, border=10)

    # A bottom row that has player information
    bottom_row = self.createBottomRow()
    box.Add(bottom_row, flag=wx.EXPAND)

    # This is magic that resizes the sizer and this frame to fit the contents
    # each time it's redrawn, otherwise we'd specify sizes above
    box.SetSizeHints(self)

    # adjust the settings for this frame
    self.SetBackgroundColour(DotsFrame.BG_WHITE)
    self.SetAutoLayout(True)
    self.SetSizer(box)
    self.Layout()

  def createBottomRow(self):
    """
      Adding a bottom row of player information including a button to submit
      their moves, the current score, and how many moves they have left
    """
    panel = wx.Panel(self)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    flags = wx.ALL|wx.EXPAND
    border_size = 25

    # Button to submit the currently selected dots as a move
    # XXX gc3: FIXME can we use wx.MouseEventsManager make this click + drag?
    submit = wx.Button(panel)
    submit.SetLabelMarkup("<big>Submit Selection</big>");
    submit.Bind(wx.EVT_BUTTON, self.onSubmitSelection)
    sizer.Add(submit, flag=flags, border=border_size);

    # force the button the left & text on the far right
    sizer.AddStretchSpacer();

    # show the score
    self._score = wx.StaticText(panel)
    self._score.SetFont(wx.Font(wx.FontInfo(18)))
    self.redrawScore()
    sizer.Add(self._score, flag=flags, border=border_size);

    # show the moves left in the game
    self._moves_left = wx.StaticText(panel)
    self._moves_left.SetFont(wx.Font(wx.FontInfo(18)))
    self.redrawMovesLeft()
    sizer.Add(self._moves_left, flag=flags, border=border_size);

    # contrast the color to the game background and return
    panel.SetBackgroundColour(DotsFrame.BG_GREY)
    panel.SetSizer(sizer)
    return panel

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

  def createGameOverScreen(self):
    # XXX gc3: FIXME make this more fun
    game_over_dialog = wx.MessageDialog(
      self,
      "Great Job!\nYour Final Score: " + str(self._game.getScore()),
      caption="Game Over!",
      style=wx.YES_NO|wx.CENTRE|wx.DIALOG_EX_METAL)
    game_over_dialog.SetYesNoLabels("New Game", "Quit")

    if (game_over_dialog.ShowModal() == wx.ID_YES):
      self.onNewGame([])
    else:
      self.onQuit([])

  def onAbout(self,  event):
    """
		  A message dialog box with an OK button
    """
    dialog = wx.MessageDialog(self, "My Dots!", "About Dots", wx.OK)
    dialog.ShowModal()

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
    if __debug__:
      print ("New game! Reset all the things");

    self._game.reset()
    self.redrawGame()

  def onSubmitSelection(self, event):
    """
      The user is requesting to lock in their selected dots and 'make their
      move', so we will execute that move and optionally redraw the board if we
      need to fill in new dots.
    """
    if __debug__:
      print ("Selection Submitted for Evaluation!")

    move_result = self._game.executeSelection()

    # if the move is not a problem, update the ui
    if (move_result != game.DotsGame.MOVE_REJECTED):
      self.redrawGame()

    # if a move ends the game, we let them know their score and give them
    # the option to quit or play again
    if (move_result == game.DotsGame.MOVE_ENDS_GAME):
      self.createGameOverScreen()

  def redrawGame(self) -> None:
    """
      Completely redraw the game based on the current state of the logic
    """
    self.redrawScore()
    self.redrawMovesLeft()
    self._board.redraw()

  def redrawScore(self) -> None:
    """
      Using the current state of the game, update the player visible display for
      their score by updating the label of the text element holding it.
    """
    self._score.SetLabel(label="Current Score: " + str(self._game.getScore()))

  def redrawMovesLeft(self) -> None:
    """
      Using the current state of the game, update the player visible display for
      the number of moves they left before the end of the game by updating the
      label of the text element holding it.
    """
    self._moves_left.SetLabel(
      label="Moves Left: " + str(self._game.getMovesLeft())
    )

  def unselectAllDots(self):
    """
      A pass through to the board so we dont break encapsulation that
      ... asks the unselects the currently selected dots.
    """
    return self._board.unselectAllDots()


###########################################################
#
# DotsBoard
#   The the dots board with dots in it you can click on
#
class DotsBoard(wx.GridSizer):
  def __init__(self, parent, game:game.DotsGame):
    wx.GridSizer.__init__(self, game.getWidth(), game.getHeight(), 0, 0)

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
        self.Add(button, y + x, flag=wx.EXPAND)

    self.Layout();  # force the re-drawing of the dots

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

    # we 'unselect' dots by telling them to toggle their visual state
    for item in self.GetChildren():
      item.GetWindow().selected(False);

############################################################
#
# DotsDot
#   The the dots a board is composed of that are like items you
#   can multi-select via dragging as you play the game
#
class DotsDot(wx.BitmapButton):
  def __init__(self, parent:DotsFrame, game:game.DotsGame, y:int, x:int):
    wx.BitmapButton.__init__(
      self,
      parent,
      wx.ID_ANY,
      bitmap=wx.BitmapBundle(DotsColor.getBitmap(game.getDotColor(y, x))),
      style=wx.BORDER_NONE, # makes the buttons look like dots
      size=wx.Size(69, 69)) # make the size match the bitmaps + 5px border

    self._y = y
    self._x = x
    self._game = game
    self._frame = parent

    self.Bind(wx.EVT_BUTTON, self.onClick)
    self.selected(False)

  def selected(self, darken=True) -> None:
    """
      If a dot is currently selected, darken its background.
      If it's not, then use the default background (white).
    """
    self.Show(False);
    self.SetBackgroundColour(
      DotsColor.BG_SELECTED if darken else DotsColor.BG_DEFAULT
    )
    self.Show(True);

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
      self._frame.unselectAllDots()
    else:
      # otherwise, just toggle the button to visually represent being selected
      self.selected(True)
