from . import db
import time
from sqlalchemy import inspect

# code cache of results
class Engine(db.Model):
 __tablename__ = 'cache'
 id = db.Column(db.Integer, primary_key=True)
 title = db.Column(db.String(128))
 path = db.Column(db.String(2048))
 lines = db.Column(db.String(2048))
 risk = db.Column(db.String(32))
 lang = db.Column(db.String(32))
 rule_id = db.Column(db.String(16))

# To return all struct for each tuple
 def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


