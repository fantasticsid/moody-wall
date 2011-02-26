import os
import wx
import ConfigParser
import common.config


def exists(item):
    foldername = make_dir(item)
    rootpath = common.config.path
    path = os.path.join(rootpath, 'image', foldername)
    if os.path.exists(path):
        return True
    else:
        return False

def make_dir(item):
    return item[0] + item[1]

def create_dir(item):
    foldername = make_dir(item)
    rootpath = common.config.path
    path = os.path.join(rootpath, 'image', foldername)
    os.makedirs(path)

def create_config_file():
    config_path = os.path.join(common.config.path, 'config.txt')
    config = ConfigParser.RawConfigParser()
    config.add_section('ScreenSize')
    mm = wx.DisplaySize()   
    width = mm[0];
    height = mm[1];
    config.set('ScreenSize', 'width', str(width))
    config.set('ScreenSize', 'height', str(height))
    configfile = open(config_path, 'wb')
    config.write(configfile)

def have_config_file():
    config_path = os.path.join(common.config.path, 'config.txt')
    if os.path.exists(config_path):
        return True
    else:
        return False

def get_screen_geometry():
    config = ConfigParser.RawConfigParser()
    config_path = os.path.join(common.config.path, 'config.txt')
    config.read(config_path)
    width = config.getint('ScreenSize', 'width')
    height = config.getint('ScreenSize', 'height')
    return (width, height)

def create_image_dir():
    imagedir = os.path.join(common.config.path, 'image')
    os.mkdir(imagedir)

def have_image_dir():
    imagedir = os.path.join(common.config.path, 'image')
    if os.path.exists(imagedir):
        return True
    else:
        return False

