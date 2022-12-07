from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from basic.Users.forms import Registration, Login, Update, ResetMail, ResetPassword
from basic.models import User
from basic import db, bcrypt
from basic.Users.utils import send_reset_mail
users = Blueprint('users', __name__)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    sup = Registration()
    if sup.validate_on_submit():
        flash(f'Account Created successfully for {sup.name.data}', 'success')
        u = User(name=sup.name.data, mail=sup.mail.data,
                 password=bcrypt.generate_password_hash(sup.password.data).decode('utf-8'))
        db.session.add(u)
        db.session.commit()
        login_user(u)
        return redirect(url_for('main.home'))
    return render_template('signup.html', title='Signup', supform=sup)


@users.route('/login', methods=['GET', 'POST'])
def login():
    lin = Login()
    if current_user.is_authenticated == True:
        return redirect(url_for('main.home'))

    if lin.validate_on_submit():
        usr = User.query.filter_by(mail=lin.mail.data).first()
        if usr and bcrypt.check_password_hash(usr.password, lin.password.data):
            login_user(usr)
            nxt = request.args.get('next')
            if nxt:
                nxt = nxt[1:]
                return redirect(url_for(nxt))
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful verify your email or password', 'danger')
    return render_template('login.html', title='Login', linform=lin)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    upd = Update()
    if upd.validate_on_submit():
        current_user.name = upd.name.data
        current_user.mail = upd.mail.data
        db.session.commit()
        flash(f'Account details updated successfully {upd.name.data}', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        upd.name.data = current_user.name
        upd.mail.data = current_user.mail
    return render_template('account.html', title='Account', actform=upd)


@users.route('/resetpassword', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetMail()
    if form.validate_on_submit():
        usr = User.query.filter_by(mail=form.mail.data).first()
        send_reset_mail(usr)
        flash('Email sent to reset password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_mail.html', form=form, title='Enter Reset Mail')


@users.route('/generatepassword/<token>', methods=['GET', 'POST'])
def newpassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    usr = User.verify_reset_token(token)
    if usr is None:
        flash('Invalid or Expired Token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usr.password = hash_pass
        db.session.commit()
        flash('Password Updated Successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('changepassword.html', form=form, title='New Password')
