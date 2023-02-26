#! /usr/bin/env python

"""
  Author: gc3
  Program:
  Date:
  Description: all the ui lives here for convenience as a learner project
"""

import wx
import game

class DotsFrame(wx.Frame):
  def __init__(self, parent, ID, title, game):
    print("XXX gc3: in Dots Frame constructor")
    self._game = game;

    wx.Frame.__init__(self, parent, ID, title, size=(800, 800))

    button = wx.Button(self, wx.ID_ANY, "Select a Blue")
    button.Bind(wx.EVT_BUTTON, self.onClick)

    button2 = wx.Button(self, wx.ID_ANY, "Select a Red")
    button2.Bind(wx.EVT_BUTTON, self.onClick2)

    panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
    panel1.SetBackgroundColour("BLUE")

    panel2 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
    panel2.SetBackgroundColour("RED")

    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(panel1, 1, wx.EXPAND)
    box.Add(panel2, 2, wx.EXPAND)
    box.Add(button, 3, wx.EXPAND)
    box.Add(button2, 4, wx.EXPAND)

    self.SetAutoLayout(True)
    self.SetSizer(box)
    self.Layout()

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

class DotsBoard():
  def __init__(self):
    print("XXX gc3: board constructor")

class DotsDot():
  def __init__(self):
    print("XXX gc3: dot constructor")
