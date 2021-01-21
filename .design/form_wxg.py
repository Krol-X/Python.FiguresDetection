#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Thu Jan 21 20:30:12 2021
#

import wx


# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((640, 480))

        # Menu Bar
        self.main_menu = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.main_menu.Append(wxglade_tmp_menu, "Open")
        wxglade_tmp_menu = wx.Menu()
        self.main_menu.Append(wxglade_tmp_menu, "Process")
        wxglade_tmp_menu = wx.Menu()
        self.main_menu.Append(wxglade_tmp_menu, "Save as...")
        self.SetMenuBar(self.main_menu)
        # Menu Bar end
        self.src_image = wx.Panel(self, wx.ID_ANY)
        self.new_image = wx.Panel(self, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("frame")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.src_image, 1, wx.EXPAND | wx.RIGHT, 1)
        sizer_1.Add(self.new_image, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def menu_hnd(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'menu_hnd' not implemented!")
        event.Skip()


# end of class MainFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
