import base64
import os

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required

from basic import db
from basic.Pics.forms import Upload, EditUpload
from basic.Pics.utils import save_picture
from basic.models import Pics

pics = Blueprint('pics', __name__)


@pics.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    upl = Upload()
    if upl.validate_on_submit():
        p = Pics(name=upl.name.data, desc=upl.desc.data, owner=current_user)
        p.img = save_picture(upl.name.data, upl.image.data)
        db.session.add(p)
        db.session.commit()
        flash(f'Image added', 'success')
        return redirect(url_for('main.home'))
    return render_template('upload.html', uplform=upl)


@pics.route('/pictures/<int:pic_id>', methods=['GET', 'POST'])
@login_required
def pictures(pic_id):
    p = Pics.query.get_or_404(pic_id)
    pictures = []
    new_pictures = {}
    path = current_app.root_path
    os.chdir(path + '/static/user_images/')
    f = open(p.img, 'rb')
    data = f.read()
    b64data = base64.b64encode(data).decode('utf-8')
    pictures.append([p.desc, b64data, p.img, p.id])
    f.close()

    _, ext = os.path.splitext(p.img)
    editupl = EditUpload()
    if editupl.validate_on_submit():
        old_name = p.img
        p.name = editupl.name.data
        p.desc = editupl.desc.data
        p.img = p.name + ext
        new_name = p.img
        db.session.commit()
        os.rename(old_name, new_name)
        flash(f'Picture details updated successfully', 'success')
        new_pictures[p.name] = [p.desc, b64data, p.img, p.id]
        return render_template('home.html', pictures=new_pictures)

    elif request.method == 'GET':
        editupl.name.data = p.name
        editupl.desc.data = p.desc

    return render_template('pictures.html', title=p.name, pics=pictures, picform=editupl)


@pics.route('/delete/<int:pic_id>', methods=['POST'])
@login_required
def delete(pic_id):
    pic = Pics.query.get_or_404(pic_id)
    db.session.delete(pic)
    db.session.commit()
    os.chdir(current_app.root_path + '/static/user_images/')
    os.remove(pic.img)
    flash(f'Picture deleted successfully', 'success')
    return redirect(url_for('main.home'))
