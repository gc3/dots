#! /usr/bin/env python

"""
  Author: gc3
  Program:
  Date:
  Description: all the ui lives here for convenience as a learner project
"""

class DotsFrame(wx.Frame):
  def __init__(self, parent, ID, title, game):
    print("XXX gc3: in Dots Frame constructor")
    print(game)

    wx.Frame.__init__(self, parent, ID, title, size=(800, 800))

    button = wx.Button(self, wx.ID_ANY, "This is resized")
    button.Bind(wx.EVT_BUTTON, self.onClick)

    panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
    panel1.SetBackgroundColour("BLUE")

    panel2 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
    panel2.SetBackgroundColour("RED")

    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(panel1, 1, wx.EXPAND)
    box.Add(panel2, 2, wx.EXPAND)
    box.Add(button, 3, wx.EXPAND)

    self.SetAutoLayout(True)
    self.SetSizer(box)
    self.Layout()

  def onClick(self, event):
    print("XXX gc3: clicked")
    print(event)

