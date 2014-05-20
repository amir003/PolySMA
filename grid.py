#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.grid

class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.CreateGrid(50, 50)


        self.SetColLabelValue(0, "1")
        self.SetColLabelValue(1, "2")
        self.SetColLabelValue(1, "3")
        
        self.SetCellValue(0, 0, "¥")

        self.SetCellValue(0, 5, "¥")
       
        self.SetRowLabelValue(1, "2")
        
        self.SetRowLabelValue(2, "3")
        
        self.SetRowLabelValue(3, "4")
        
        self.SetCellValue(3, 1, "¥")
        self.SetRowLabelValue(4, "5")
        
        self.SetRowLabelValue(5, "6")
        self.SetCellValue(5, 1, "¥")
        self.SetRowLabelValue(6, "7")
        
        self.SetRowLabelValue(7, "8")
        
        self.SetRowLabelValue(14, "15")
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


