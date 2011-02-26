import os
import sys
import random
from PIL import Image

def set_image(img):
    if sys.platform in ('linux2',):
        import commands
        command = "gconftool-2 --set /desktop/gnome/background/picture_filename --type string '%s'" % img
        status, output = commands.getstatusoutput(command)
    elif sys.platform in ('win32',):
        import ctypes
        orig_img = Image.open(img)
        bmppath = os.path.join(os.getcwd(), 'image.bmp')
        orig_img.save(bmppath, 'BMP')
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, bmppath, 0)

def change_wall(file_list):
    """
    file_list: absolute path of files
    """
    if len(file_list) == 0:
        return
    file = file_list[random.randrange(0, len(file_list))]
    set_image(file)

if __name__ == '__main__':
    files = sys.argv[1:]
    files = map(os.path.abspath, files)
    change_wall(files)
