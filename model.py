from app import db, app
from flask_security import RoleMixin, UserMixin



roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):  # 权限
    # __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):  # 用户
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    integral = db.Column(db.Integer, nullable=False,default=0)
    uncivilized = db.Column(db.Integer, nullable=False,default=0)
    blacklist = db.Column(db.Integer, nullable=False,default=0)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Trash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    community = db.Column(db.String(128), nullable=False)
    recyclable_trash = db.Column(db.Integer, nullable=False,default=0)
    non_recyclable_trash = db.Column(db.Integer, nullable=False,default=0)
    hazardous_trash = db.Column(db.Integer, nullable=False,default=0)
    kitchen_trash = db.Column(db.Integer, nullable=False,default=0)
    time = db.Column(db.DateTime, nullable=False)

class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commodity = db.Column(db.String(128), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    integral = db.Column(db.Integer, nullable=False,default=1000)


class Popular_science(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    classification = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    introduction = db.Column(db.Text)

class Recycling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    classification = db.Column(db.String(128), nullable=False)
    image_path = db.Column(db.String(128), nullable=False)
    pickup_code = db.Column(db.Integer, nullable=False)
    recycling = db.Column(db.Integer, nullable=False,default=0)


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(128), nullable=False)
    recyclable_trash = db.Column(db.Integer, nullable=False, default=0)
    non_recyclable_trash = db.Column(db.Integer, nullable=False, default=0)
    hazardous_trash = db.Column(db.Integer, nullable=False, default=0)
    kitchen_trash = db.Column(db.Integer, nullable=False, default=0)
    recyclable_trash_original = db.Column(db.Integer, nullable=False, default=0)
    non_recyclable_trash_original = db.Column(db.Integer, nullable=False, default=0)
    hazardous_trash_original = db.Column(db.Integer, nullable=False, default=0)
    kitchen_trash_original = db.Column(db.Integer, nullable=False, default=0)


class Linshi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    image_path = db.Column(db.String(128), nullable=False)
    cls = db.Column(db.Text, nullable=False)
    cls_number = db.Column(db.String(128), nullable=False)
    cls_4 = db.Column(db.String(128), nullable=False)
    cls_4_counts = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()
