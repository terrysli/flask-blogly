"""Seed file to make sample data for users db"""

from models import User, db
from app import app

db.drop_all()
db.create_all()

alan_alda = User(first_name='Alan', last_name='Alda')
joel_burton = User(first_name='Joel', last_name='Burton')
jane_smith = User(first_name='Jane', last_name='Smith')

db.session.add(alan_alda)
db.session.add(joel_burton)
db.session.add(jane_smith)

db.session.commit()

