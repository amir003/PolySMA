#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.grid

class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.CreateGrid(50, 50)
        
        self.SetRowLabelSize(50)
        self.SetColLabelSize(30)#size of a col label (height to be precise) and so the col
        
        #avoid resize moification by the user of the grid
        self.EnableDragColSize(0)
        self.EnableDragRowSize(0)
        self.EnableDragGridSize(0)
        
        #set the size of all the col
        for i in range(50):
          self.SetColLabelValue(i, str(i+1))#set the label
          self.SetColSize(i, 30)#set the size of all the col
        
        self.SetCellValue(0, 0, "¥")
        self.SetCellTextColour(0,0,'red') #colorie le texte
        self.SetCellValue(0, 5, "¥")
        self.SetCellValue(5, 1, "¥")
        self.SetCellValue(14, 1, "¥")
        

class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Prédicteur de structure protéique",
                size=(800, 600))
        grid = SimpleGrid(self)

app = wx.PySimpleApp()
frame = TestFrame(None)
frame.Show(True)
app.MainLoop()


