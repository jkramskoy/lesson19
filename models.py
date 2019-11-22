import os
from sqla_wrapper import SQLAlchemy
db = SQLAlchemy(os.getenv("DATABASE_URL","sqlite:///losalhost.sqlite")) #connection to database

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    secret_number = db.Column(db.Integer)
