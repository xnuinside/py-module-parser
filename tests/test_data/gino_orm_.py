import gino as g
from gino import Gino

db = Gino()


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    db = db.Column(db.String())
    created_at = db.Column(db.TIMESTAMP())
    updated_at = db.Column(db.TIMESTAMP())
    country_code = db.Column(db.Integer())
    default_language = db.Column(db.Integer())
