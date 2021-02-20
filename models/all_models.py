from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class OwnerModel(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(30), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False, unique=True)

    def __init__(self, owner_name, username, password):
        # self.id = _id
        self.owner_name = owner_name
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

    def __repr__(self):
        return f'<Owner {self.owner_name}'


class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False, unique=False)
    task_status = db.Column(db.String(15))
    task_priority = db.Column(db.String(10))
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"))
    owner = db.relationship("OwnerModel", backref="tasks")
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    due_date = db.Column(db.DateTime, nullable=True,default=datetime.datetime.today())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Tasks {self.task_name}'

db.create_all()








