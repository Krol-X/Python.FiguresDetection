import wx
from resource import *


#####################################################################
# wx.Frame MainFrame
#####################################################################
class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # Инициализация состояния
        # ...

        # Инициализация главного окна
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((640, 480))

        # Инициализация меню
        self.main_menu = wx.MenuBar()
        self.init_mainmenu()

        # Инициализация областей вывода изображений
        self.src_image = wx.Panel(self, ID_SRCIMAGE)
        self.new_image = wx.Panel(self, ID_NEWIMAGE)

        # Задание свойств окна
        self.SetTitle(STR_CAPTION)

        # Задание обработчиков событий
        self.Bind(wx.EVT_CLOSE, self.onClose, id=wx.ID_ANY)
        self.Bind(wx.EVT_MENU, self.onMenu, id=wx.ID_ANY)

        # Конец инциализации главного окна
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.src_image, 1, wx.EXPAND | wx.RIGHT, 1)
        sizer_1.Add(self.new_image, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

    def init_mainmenu(self):
        for id in range(len(MENU)):
            tmp_menu = wx.Menu()
            cur = MENU[id]
            for i in range(len(cur)):
                if i != 0:
                    tmp_menu.Append(ID_MENU + id * NEXT_ID + i, cur[i])
            self.main_menu.Append(tmp_menu, cur[0])
        self.SetMenuBar(self.main_menu)

    def onClose(self, event):
        self.Destroy()

    def onMenu(self, event):
        if event.Id == ID_OPEN:
            pass
        if event.Id == ID_SAVEAS:
            pass
        if event.Id == ID_EXIT:
            self.onClose(self)
        if event.Id == ID_DETECT:
            print("Detect...")