#!/usr/bin/env python

#-----------------------------------------------------------------------
# models.py
#-----------------------------------------------------------------------

from tangelo import db, login_manager
from flask_login import UserMixin
from tangelo.models_service import JSONEncodedDict
from datetime import datetime

#-----------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    middle_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120), nullable=False)
    display_name = db.Column(db.String(30), default='')
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)

    widgets = db.relationship('Widget', secondary='subscriptions', passive_deletes=True)
    widgets_admin = db.relationship('Widget', secondary='administrators', passive_deletes=True)
    posts = db.relationship('Post', backref='author', cascade="all,delete", lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return f"User('{self.netid}')"

class Widget(db.Model):
    __tablename__ = 'widgets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    access_type = db.Column(db.String(), default='public')
    post_type = db.Column(db.String(), default='public')
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)

    admins = db.relationship('User', secondary='administrators', passive_deletes=True)
    users = db.relationship('User', secondary='subscriptions', passive_deletes=True)
    posts = db.relationship('Post', backref='widget', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return f"Widget('{self.name}', '{self.description}')"

class AdminAssociation(db.Model):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True)
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id', ondelete='CASCADE'))

    user = db.relationship(User, backref=db.backref("administrators", cascade="all, delete-orphan"))
    widget = db.relationship(Widget, backref=db.backref("administrators", cascade="all, delete-orphan"))

    __mapper_args__ = {
        'confirm_deleted_rows' : False
    }

    def __repr__(self):
        return f"AdminAssociation(Admin: '{self.user.netid}', Widget: '{self.widget.name}')"

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)
    # admin = db.Column(db.Boolean, unique=False, default=False)
    grid_location = db.Column(JSONEncodedDict, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id', ondelete='CASCADE'))

    user = db.relationship(User, backref=db.backref("subscriptions", cascade="all, delete-orphan"))
    widget = db.relationship(Widget, backref=db.backref("subscriptions", cascade="all, delete-orphan"))

    __mapper_args__ = {
        'confirm_deleted_rows' : False
    }

    def __repr__(self):
        return f"Subscription('{self.user}', '{self.widget}')"

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id', ondelete='CASCADE'))
    content = db.Column(db.String(100), nullable=False)
    # body = db.Column(db.Text, nullable=True)
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.body}', '{self.create_dttm}')"
