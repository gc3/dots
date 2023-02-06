#! /usr/bin/env python3

"""
  Author: gc3
  Program: dots game
  Date:
  Description: wanna relearn python
"""

import wx

class DotsFrame(wx.Frame):
  def __init__(self, parent, ID, title):
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

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = DotsFrame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()
