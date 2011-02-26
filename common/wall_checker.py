import os
import urllib
from common import config, helper
import re

import logging
logging.basicConfig(level=logging.DEBUG)

rooturl = "http://www.smashingmagazine.com/tag/wallpapers/"
pattern_post = "http://www.smashingmagazine.com/\d+/\d+/\d+/desktop-wallpaper-calendar-\w+-\d+/"
pattern_image = "http://media.smashingmagazine.com/cdn_smash/wp-content/uploads/uploader/wallpapers/.*?/.*?-\d+x\d+.(?:jpg|png)"

def check_update():
    latest_item = check_latest()
    if not helper.exists(latest_item[-2:]):
        helper.create_dir(latest_item[-2:])
    for image in download_new_item(latest_item):
        save_image(image, latest_item)

def check_latest():
    conn = urllib.urlopen(rooturl)
    page = conn.read()
    conn.close()
    latest_url = re.findall(pattern_post, page)[0]
    logging.debug('latest url found: %s' % latest_url)
    if not latest_url:
        return None
    m = re.match('.*(\d+)/(\d+)/(\d+).*-(\w+)-(\d+).*', latest_url)
    return (latest_url, ) + m.groups()[-2:]

def download_new_item(latest_item):
    screen_geometry = helper.get_screen_geometry()
    url = latest_item[0]
    folder = helper.make_dir(latest_item[-2:])
    conn = urllib.urlopen(url)
    page = conn.read()
    conn.close()
    images = re.findall(pattern_image, page)
    images = list(set(images))
    for image in images:
        m = re.match('.*/(.*)', image)
        filename = m.groups()[0]
        m = re.match('.*?(\d+)x(\d+).*', filename)
        (width, height) = list(map(int, m.groups()[:2]))
        if not (width, height) == screen_geometry:
            continue
        if os.path.exists(os.path.join(config.path, 'image', folder, filename)):
            continue
        logging.debug('downloading image: %s\n' % image)
        conn = urllib.urlopen(image)
        image_data = conn.read()
        conn.close()
        yield (filename, image_data)

def save_image(imagetuple, itemtuple):
    folder = helper.make_dir(itemtuple[-2:]) # make_dir should return a dir, not create one
    filename = imagetuple[0]
    image = imagetuple[1]
    path = os.path.join(config.path, 'image', folder, filename)
    print "saving image", filename
    f = open(path, 'wb')
    f.write(image)
    f.close()
