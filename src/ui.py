#! /usr/bin/env python

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: all the ui lives here for convenience as a learner project
"""

import wx
import game
from util import DotsColor, decodeMouseEvent

###########################################################
#
# Dots Frame
#   The main frame for a dots game that contains the board
class DotsFrame(wx.Frame):

  # Some default colors to be reused
  BG_GREY   = wx.Colour(50, 50, 50, 255)
  BG_WHITE  = wx.Colour(255, 255, 255, 255)

  # Commonly used arguments for sizers
  SIZER_FLAGS = wx.ALIGN_CENTER | wx.ALL
  SIZER_BORDER = 25


  def __init__(self, parent, ID, title, dots_game:game.DotsGame):
    wx.Frame.__init__(self, parent, ID, title)

    self._game = dots_game

    self.FONT_BIG = wx.Font(wx.FontInfo(18))
    self.FONT_GIANT = wx.Font(wx.FontInfo(30).Bold(True))

    # Setting up the menus and menubar.
    self.createFileMenus()

		# Setting up the dots board in a simple layout
    box_sizer = wx.BoxSizer(wx.VERTICAL)

    self._board = DotsBoard(self, self._game)
    box_sizer.Add(self._board, flag=wx.ALL|wx.EXPAND, border=10)

    # A bottom row that has player information
    bottom_row = self.createBottomRow()
    box_sizer.Add(bottom_row, flag=wx.EXPAND)

    # This is magic that resizes the sizer and this frame to fit the contents
    # each time it's redrawn, otherwise we'd specify sizes above
    box_sizer.SetSizeHints(self)

    # adjust the settings for this frame
    self.SetBackgroundColour(DotsFrame.BG_WHITE)
    self.SetSizer(box_sizer)
    self.Layout()

  ###
  # UI Element Creation Helpers
  #
  def createBottomRow(self) -> wx.Panel:
    """
      Adding a bottom row of player information including a button to submit
      their moves, the current score, and how many moves they have left
    """
    panel = wx.Panel(self)
    sizer = wx.BoxSizer(wx.HORIZONTAL)

    # show the score
    self._score = wx.StaticText(panel)
    self._score.SetFont(self.FONT_BIG)
    self.redrawScore()

    # show the moves left in the game
    self._moves_left = wx.StaticText(panel)
    self._moves_left.SetFont(self.FONT_BIG)
    self.redrawMovesLeft()

    sizer.AddStretchSpacer()
    sizer.Add(self._score, flag=self.SIZER_FLAGS, border=self.SIZER_BORDER)
    sizer.Add(self._moves_left, flag=self.SIZER_FLAGS, border=self.SIZER_BORDER)
    sizer.AddStretchSpacer()

    # contrast the color to the game background and return
    panel.SetBackgroundColour(DotsFrame.BG_GREY)
    panel.SetSizer(sizer)
    return panel

  def createFileMenus(self) -> None:
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

  def createGameOverDialog(self) -> None:
    """
      Helper to create the end game 'screen', which is actually a modal dialog
    """
    dialog = wx.Dialog(self, title="Game Over", style=wx.SYSTEM_MENU)

    # Top: A panel to hold ...
    bmp = wx.Bitmap('../images/game_over.jpg')
    top_panel = wx.Panel(dialog, size=wx.Size(bmp.GetWidth(), bmp.GetHeight()))
    top_panel_sizer = wx.BoxSizer(wx.VERTICAL)

    #   1. a pretty background image
    wx.StaticBitmap(top_panel, bitmap=bmp)

    #   2. a message to show the user their score and salute them
    message = wx.StaticText(top_panel, style=wx.ALIGN_CENTRE_HORIZONTAL)
    message.SetFont(self.FONT_GIANT)
    message.SetLabel(
      "Great Job!\n \n" +
      "Your Final Score: %d \n \n \n" % self._game.getScore() +
      "Start a New Game?"
    )
    top_panel_sizer.AddSpacer(
      (bmp.GetHeight() - message.GetClientSize()[1]) // 2 # align vertically
    )
    top_panel_sizer.Add(message, flag=wx.ALIGN_CENTER)    # align horizontally
    top_panel.SetSizer(top_panel_sizer)

    # Bottom:  Buttons to allow for starting a new game or quitting
    buttons = wx.Panel(dialog, size=wx.Size(bmp.GetWidth(), bmp.GetHeight()//5))
    button_sizer = wx.BoxSizer(wx.HORIZONTAL)
    buttons.SetSizer(button_sizer)

    button_sizer.AddStretchSpacer()
    new_g_btn = wx.Button(buttons, id=wx.ID_OK, label="\nNew Game\n")
    new_g_btn.SetFont(self.FONT_BIG)
    button_sizer.Add(new_g_btn, flag=self.SIZER_FLAGS, border=self.SIZER_BORDER)

    quit_btn = wx.Button(buttons, id=wx.ID_CANCEL, label="\nQuit\n")
    quit_btn.SetFont(self.FONT_BIG)
    button_sizer.Add(quit_btn, flag=self.SIZER_FLAGS, border=self.SIZER_BORDER)
    button_sizer.AddStretchSpacer()

    # layout the top & bottom
    dialog_sizer = wx.BoxSizer(wx.VERTICAL)
    dialog_sizer.Add(top_panel)
    dialog_sizer.AddStretchSpacer() # force the top and bottom apart
    dialog_sizer.Add(buttons, flag=wx.EXPAND)

    dialog.SetSizerAndFit(dialog_sizer)
    dialog.Centre()

    # show this dialog and do what the player indicates
    self.HideWithEffect(wx.SHOW_EFFECT_ROLL_TO_BOTTOM, timeout=500)
    if (dialog.ShowModal() == wx.ID_OK):
      self.onNewGame([])
    else:
      self.onQuit([])

  ###
  # Event Handlers
  #
  def onAbout(self,  event) -> None:
    """
		  A message dialog box with an OK button
    """
    dialog = wx.MessageDialog(self, "My Dots!", "About Dots", wx.OK)
    dialog.ShowModal()

  def onQuit(self, event) -> None:
    """
      Someone hit the quit button!
    """
    if __debug__:
      print ("Someone hit the quit button!")

    self.Destroy()

  def onNewGame(self, event) -> None:
    """
      Someone has requested a new game. Reset the game logic and
      the board that represents it afterwards
    """
    if __debug__:
      print ("New game! Reset all the things")

    if (self.IsShown()):
      self.HideWithEffect(wx.SHOW_EFFECT_ROLL_TO_BOTTOM, timeout=500)
    else:
      self.ShowWithEffect(wx.SHOW_EFFECT_ROLL_TO_TOP, timeout=500)

    self._game.reset()
    self.redrawGame()

  ###
  # (re) Drawing the game contents
  #
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
    self._score.SetLabel("Current Score: %d" % self._game.getScore())

  def redrawMovesLeft(self) -> None:
    """
      Using the current state of the game, update the player visible display for
      the number of moves they left before the end of the game by updating the
      label of the text element holding it.
    """
    self._moves_left.SetLabel("Moves Left: %d" % self._game.getMovesLeft())

  ###
  # Selection of Dots
  #
  def executeSelection(self) -> None:
    """
      The user is locking in their selected dots and 'make their move', so we
      will execute that move and optionally redraw the board if we need to fill
      in new dots.
    """
    move_result = self._game.executeSelection()

    # if the move is not a problem, update the ui
    if (move_result != game.DotsGame.MOVE_REJECTED):
      self.redrawGame()

    # if a move ends the game, we let them know their score and give them
    # the option to quit or play again
    if (move_result == game.DotsGame.MOVE_ENDS_GAME):
      self.createGameOverDialog()

###########################################################
#
# DotsBoard
#   The the dots board with dots in it you can click on
#
class DotsBoard(wx.Panel):
  def __init__(self, parent, dots_game:game.DotsGame):
    wx.Panel.__init__(self, parent)

    self._game = dots_game
    self._parent = parent
    self._sizer = wx.GridSizer(
      dots_game.getWidth(),
      dots_game.getHeight(),
      0, 0
    )

    self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
    self.SetSizer(self._sizer)
    self.redraw()

  def onMouseEvent(self, event):
    """
      Handle any incoming mouse events to the board. This is used to make
      selecting dots by the player work with dragging.
    """

    # turn the screen coordinates for this event to an (x, y) on the board
    mouse_position = self.ScreenToClient(wx.GetMousePosition())
    y = mouse_position.y // DotsDot.Y_SIZE
    x = mouse_position.x // DotsDot.X_SIZE

    if __debug__:
      print(
        "Mouse Event(%d, %s) at position%s dot(%d, %d)" % (
        event.GetEventType(), decodeMouseEvent(event), str(mouse_position), y, x
      ))

    # if the player clicks the left mouse button at all, it indicates an
    # intention to select teh dot under the cursor
    mouse_state = wx.GetMouseState()
    if (mouse_state.LeftIsDown()):
      if (not self._game.isGameOver()):
        self.selectDot(y, x)

    # otherwise, we just try to execute whatever is in the current selection if
    # there is any. this will simulate dragging and clicking,
    else:
      self._parent.executeSelection()

    return True

  def redraw(self):
    """
      Redraw the board appearance by getting rid of all the dots and recreating
      them using the game data that we already have.

      NB: If you haven't updated the game data all, this will appear to do
          nothing, so update that BEFORE calling this.
    """

    # get rid of the old dots
    self._sizer.Clear(True)

    for y in range(self._game.getHeight()):
      for x in range(self._game.getWidth()):
        # recreate dots to get new colors
        dot = DotsDot(self, self._game, y, x)

        # reselect previously selected dots
        dot.selected(self._game.isSelected(dot._y, dot._x))
        self._sizer.Add(dot, y + x, flag=wx.EXPAND)

    # force the re-drawing of board
    self.Layout()

  def selectDot(self, y: int, x: int) -> bool:
    """
      Select the dot at the given coordinates and redraw the board if there's
      any useful changes to show.

      Return if this dot was selected.
    """
    selected = self._game.selectDot(y, x)
    if (not selected):
      # if we didnt successfully add this dot to the current selection,
      # then we ought to reset the selection in the game logic and ui, so the
      # player can try again.
      self._game.clearSelection()
      self.unselectAllDots()

    # we redraw the board to reflect the new state of changed dots
    self.redraw()
    return selected

  def unselectAllDots(self):
    """
      Make all the dots appear to be unselected by telling them to toggle
      their visual state
    """
    for dot in self.GetChildren():
      dot.selected(False)

############################################################
#
# DotsDot
#   The the dots a board is composed of that are either selected or not
#
class DotsDot(wx.StaticBitmap):

  Y_SIZE = 69 # make Y size match the bitmaps + 5px border
  X_SIZE = 69 # make X size match the bitmaps + 5px border

  def __init__(self, parent:DotsBoard, dots_game:game.DotsGame, y:int, x:int):
    wx.StaticBitmap.__init__(
      self,
      parent,
      wx.ID_ANY,
      bitmap=wx.BitmapBundle(DotsColor.getBitmap(dots_game.getDotColor(y, x))),
      size=wx.Size(self.X_SIZE, self.Y_SIZE)
    )

    self._y = y
    self._x = x
    self.selected(False)

  def selected(self, darken=True) -> None:
    """
      If a dot is currently selected, darken its background.
      If it's not, then use the default background (white).
    """
    self.Show(False)
    self.SetBackgroundColour(
      DotsColor.BG_SELECTED if darken else DotsColor.BG_DEFAULT
    )
    self.Show(True)
