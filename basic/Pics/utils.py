import os
from flask import current_app


def save_picture(name, imgfile):
    _, ext = os.path.splitext(imgfile.filename)
    img = name + ext
    pic_path = os.path.join(current_app.root_path + "/static/user_images/" + img)
    imgfile.save(pic_path)
    return img
