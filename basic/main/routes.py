import base64
import os

from flask import Blueprint, render_template, current_app
from flask_login import current_user
from basic.models import User, Pics

main = Blueprint('main', __name__)


@main.route('/home')
def home():
    usr = User.query.filter_by(name=current_user.name).first()
    pics = Pics.query.filter_by(user_id=usr.id)
    pictures = {}

    path = current_app.root_path
    os.chdir(path + '/static/user_images/')
    for pic in pics:
        f = open(pic.img, 'rb')
        data = f.read()
        b64data = base64.b64encode(data).decode('utf-8')
        f.close()
        pictures[pic.name] = [pic.desc, b64data, pic.img, pic.id]

    return render_template('home.html', pictures=pictures)
