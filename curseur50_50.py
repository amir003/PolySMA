#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.grid


class MyFrameName(wx.Frame):

    def __init__(self,parent,id): # constructeur de fonction
        wx.Frame.__init__(self,parent,id,'Prédicteur de structure protéique',size=(800,600))

        self.panel = wx.Panel(self)

        status=self.CreateStatusBar()
        menubar=wx.MenuBar()

        first=wx.Menu()
        second=wx.Menu()

        menubar.Append(first,"File")
        first.Append(101,"New","New File")
        first.Append(102,"Open...","Open new file")

        menubar.Append(second,"Edit")

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.dosomething, id=101)


        

        self.slider_01=wx.Slider(self.panel, -1, 25, 1, 50, pos=(50,50), size=(500,-1), \
            style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.slider_01.SetTickFreq(5,1)
        self.slider_01.SetDimensions(100, 100, 350, -1)

        self.slider_02 = wx.Slider(self.panel, 101, 25, 1, 50, pos=(50,50), size=(250,-1), \
            style=wx.SL_VERTICAL | wx.SL_AUTOTICKS | wx.SL_LABELS )
        self.slider_02.SetDimensions(10, 150, -1, 350)
        self.Bind(wx.EVT_SCROLL, self.dosomething, id=101)

    def dosomething(self, event):
    	wx.StaticText(self.panel,-1,"Hello menu, what's up",(130,60))
        if self.slider_02.GetValue() == 25:
            wx.StaticText(self.panel,-1,"Slider hits 25",(320,320))         
        #print self.slider_02.GetValue()

if __name__=='__main__':    
    app=wx.PySimpleApp()
    frame=MyFrameName(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
