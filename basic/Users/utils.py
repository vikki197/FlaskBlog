from basic import mail
from flask_mail import Message
from flask import url_for


def send_reset_mail(usr):
    token = usr.get_reset_token()
    msg = Message('Password Reset Request', sender="Noreply@basic.com", recipients=[usr.mail])
    msg.body = f''' To rest password visit the following link
{url_for('newpassword', token=token, _external=True)}    
If you did  not make this request simply ignore this mail and no changes will occur
'''
    mail.send(msg)
