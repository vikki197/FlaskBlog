from basic import db,login_manager
from flask import current_app
from flask_login import UserMixin
from datetime import datetime as dt
from pytz import timezone
from itsdangerous import TimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique = True,nullable = False)
    mail = db.Column(db.String(120),unique = True,nullable = False)
    password = db.Column(db.String(60),unique = True,nullable = False)
    pic = db.relationship('Pics',backref = 'owner',lazy=True)

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'],'confirmation')
        return s.dumps({'user_id':self.id})

    @staticmethod
    def verify_reset_token(token,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],'confirmation')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.name}','{self.mail}')"

class Pics(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True,nullable=False)
    img = db.Column(db.String(20),nullable=False,default='default.jpg')
    desc = db.Column(db.Text)
    date_uploaded = db.Column(db.DateTime,nullable=False,default = dt.now(timezone('Asia/Kolkata')))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Pic('{self.name}','{self.desc}','{self.date_uploaded}')"
