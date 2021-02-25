import wx
import cv2 as cv

from tools import *
from engine import *
from resource import *


#####################################################################
# wx.ScrolledWindow MyScrolledFrame
#####################################################################

class MyScrolledFrame(wx.ScrolledWindow):
    def __init__(self, parent, panel_id=wx.ID_ANY):
        self.parent = parent
        wx.ScrolledWindow.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        self.frame = wx.Panel(self, panel_id)
        self.frame.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.frame.SetSize(0, 0)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.frame, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(sizer)

        self.SetScrollRate(10, 10)
        self.EnableScrolling(True, True)
        self.onInnerSizeChanged()

    def setNewSize(self, xy):
        self.frame.SetMinSize(xy)
        self.frame.SetSize(xy)
        self.onInnerSizeChanged()

    def onInnerSizeChanged(self):
        w, h = self.frame.GetMinSize()
        self.SetVirtualSize((w, h))


#####################################################################
# wx.Frame MainFrame
#####################################################################

class MainFrame(wx.Frame):
    wildcard = "All supported formats|*.bmp;*.jpg;*.jpeg;*.png" \
               "|BMP (*.bmp)|*.bmp" \
               "|JPEG (*.jpg; *.jpeg)|*.jpg;*.jpeg" \
               "|PNG (*.png)|*.png" \
               "|All files (*.*)|*.*"
    image = None
    newimage = None

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
        self.splitter = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3D | wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(64)
        self.frame_src = MyScrolledFrame(self.splitter, ID_SRCIMAGE)
        self.frame_new = MyScrolledFrame(self.splitter, ID_NEWIMAGE)
        self.update_size()

        # Задание свойств окна
        self.SetTitle(STR_CAPTION)

        # Задание обработчиков событий
        self.Bind(wx.EVT_CLOSE, self.onClose, id=wx.ID_ANY)
        self.Bind(wx.EVT_MENU, self.onMenu, id=wx.ID_ANY)
        self.frame_src.frame.Bind(wx.EVT_PAINT,
                                  lambda e: self.draw_frame(self.frame_src.frame, self.image))
        self.frame_new.frame.Bind(wx.EVT_PAINT,
                                  lambda e: self.draw_frame(self.frame_new.frame, self.newimage))

        # Завершение инциализации главного окна
        self.splitter.SplitVertically(self.frame_src, self.frame_new)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.splitter, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

    def init_mainmenu(self):
        for Id in range(len(MENU)):
            tmp_menu = wx.Menu()
            cur = MENU[Id]
            for i in range(len(cur)):
                if i != 0:
                    tmp_menu.Append(ID_MENU + Id * NEXT_ID + i, cur[i])
            self.main_menu.Append(tmp_menu, cur[0])
        self.SetMenuBar(self.main_menu)

    #
    # Обработчики событий
    #
    def onClose(self, event=None):
        self.Destroy()

    def onMenu(self, event):
        if event.Id == ID_OPEN:
            self.open_file()
        elif event.Id == ID_SAVEAS:
            self.save_file()
        elif event.Id == ID_EXIT:
            self.onClose()
        elif event.Id == ID_DETECT:
            self.detect()
        else:
            pass

    #
    # Методы
    #
    def open_file(self):
        dialog = wx.FileDialog(None, message="Open", defaultDir="",
                               wildcard=self.wildcard, style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.load_file(dialog.GetPath())

    def load_file(self, name):
        img = loadimage_cv(name)
        if img is None:
            wx.MessageDialog(self, 'Cannot open "' + name + '"!', caption="Error!", style=wx.OK | wx.ICON_ERROR) \
                .ShowModal()
        else:
            self.image = img
            self.newimage = None
            self.update_size()
            self.Refresh()

    def save_file(self):
        if self.newimage is None:
            return
        dialog = wx.FileDialog(None, message="Save as...", defaultDir="",
                               wildcard=self.wildcard, style=wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            saveimage_cv(dialog.GetPath(), self.newimage)

    def draw_frame(self, frame, image):
        if image is not None:
            dc = wx.BufferedPaintDC(frame)
            dc.DrawBitmap(toWxBitmap(image), 0, 0)

    def update_size(self):
        self.frame_src.setNewSize(get_imagesize(self.image))
        self.frame_new.setNewSize(get_imagesize(self.newimage))

    def detect(self):
        result, self.newimage = detect_cv(self.image)
        for name, coord in result.items():
            for xy in coord:
                cv.putText(self.newimage, name, xy, cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        self.update_size()
        self.Refresh()
