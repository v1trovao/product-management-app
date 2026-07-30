# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),unique=True,nullable=False)

    def __repr__(self):
        return self.name