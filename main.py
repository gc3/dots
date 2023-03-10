#! /usr/bin/env python3

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: wanna relearn python
"""

import wx
import wx.adv
import game
import ui

# Create a new app, don't redirect stdout/stderr to a window.
app = wx.App(False)

# game logic fed to the UI so it can react
game = game.DotsGame(max_moves=20)

# Throw up a splash screen while the game loads
bitmap = wx.Bitmap('images/splash.png', wx.BITMAP_TYPE_PNG)
wx.adv.SplashScreen(
  bitmap,
  wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
  1500,
  None
)
wx.Yield()

# instantiate the ui
frame = ui.DotsFrame(None, wx.ID_ANY, "Dots by gc3", game)
frame.Centre()
frame.Show(True)

# go go go!
app.MainLoop()
