#! /usr/bin/env python3

"""
  Author: gc3
  Program: dots game
  Date:
  Description: wanna relearn python
"""

import wx

# Create a new app, don't redirect stdout/stderr to a window.
app = wx.App(False)

# game logic fed to the UI so it can react
game = DotsGame()

# instantiate the ui
frame = DotsFrame(None, wx.ID_ANY, "Dots by gc3", game)
frame.Show(True)

# go go go!
app.MainLoop()
