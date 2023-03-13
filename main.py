#! /usr/bin/env python3

"""
  Author: gc3
  Program: Dots, the game
  Date: March, 2023
  Description: wanna relearn python
"""

import argparse
import wx
import game
import ui
import util

PROGRAM_NAME  = "Dots by gc3"
DEFAULT_MOVES = 20

# Parse any command line arguments
parser = argparse.ArgumentParser(
  prog=PROGRAM_NAME,
  description="A fun game of removing dots for high scores!"
)
parser.add_argument("-m", "--moves",  type=int, default=DEFAULT_MOVES)
args = parser.parse_args()

if __debug__:
  print ("Commandline Arguments:\n" + " " + str(args))

# Create a new app, don't redirect stdout/stderr to a window.
app = wx.App(False)

# game logic fed to the UI so it can react
game = game.DotsGame(max_moves=args.moves)

# Throw up a splash screen while the game loads
util.createSplashScreen()

# instantiate the ui
frame = ui.DotsFrame(None, wx.ID_ANY, PROGRAM_NAME, game)
frame.Centre()
frame.Show(True)

# go go go!
app.MainLoop()
