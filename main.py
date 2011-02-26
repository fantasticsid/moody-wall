import os
import wx

from common.wall_checker import check_update
from common.wall_changer import change_wall
from common.config import path
from common.helper import have_config_file, create_config_file
from common.helper import have_image_dir, create_image_dir
import random

import logging
logging.basicConfig(level=logging.DEBUG)

import threading

update_lock = threading.Lock()

def threaded_check_wall():
    if update_lock.acquire(False):
        try:
            check_update()
            print 'updated'
        except:
            pass
        update_lock.release()
    else:
        print 'already updating'

def update_wall():
    rootimagedir = os.path.join(path, 'image')
    months = os.listdir(rootimagedir)
    if len(months) == 0:
        return
    month = months[random.randint(0, len(months)-1)]
    imagedir = os.path.join(rootimagedir, month)
    images = []
    for i in os.listdir(imagedir):
        images.append(os.path.join(imagedir, i))
    change_wall(images)

class MyTaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)

        self.frame = frame
        self.SetIcon(wx.Icon('icon.png', wx.BITMAP_TYPE_PNG), 'moody wall')
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=3)
        self.Bind(wx.EVT_MENU, self.OnTaskBarUpdateWall, id=4)
        self.Bind(wx.EVT_MENU, self.OnTaskBarCheckUpdate, id=5)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(3, 'Close')
        menu.Append(4, 'Change Wallpaper')
        menu.Append(5, 'Update Wallpaper')
        return menu

    def OnTaskBarClose(self, event):
        self.frame.Close()

    def OnTaskBarActivate(self, event):
        if not self.frame.IsShown():
            self.frame.Show()

    def OnTaskBarDeactivate(self, event):
        if self.frame.IsShown():
            self.frame.Hide()
            
    def OnTaskBarUpdateWall(self, event):
        update_wall()
        
    def OnTaskBarCheckUpdate(self, event):
        t = threading.Thread(target=threaded_check_wall, args=())
        t.start()

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, (-1, -1), (200, 200))

        self.tskic = MyTaskBarIcon(self)
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.tskic.Destroy()
        self.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'moody wall')
        frame.Show(True)
        self.SetTopWindow(frame)
        frame.Hide()
        if not have_config_file():
            create_config_file()
        if not have_image_dir():
            create_image_dir()
        return True


if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
