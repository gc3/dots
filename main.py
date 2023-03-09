#! /usr/bin/env python3

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: wanna relearn python
"""

import wx
import game
import ui

# Create a new app, don't redirect stdout/stderr to a window.
app = wx.App(False)

# game logic fed to the UI so it can react
game = game.DotsGame(max_moves=2)

# instantiate the ui
frame = ui.DotsFrame(None, wx.ID_ANY, "Dots by gc3", game)
frame.Show(True)

# go go go!
app.MainLoop()
