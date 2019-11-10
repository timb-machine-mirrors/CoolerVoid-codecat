from . import db
import time
from sqlalchemy import inspect

# ID,Screenshot,Address,Date ,Status
class Rules(db.Model):
 __tablename__ = 'rules'
 id = db.Column(db.Integer, primary_key=True)
 lang = db.Column(db.String(32))
 title = db.Column(db.String(128),unique=True)
 description = db.Column(db.Text)
 level = db.Column(db.String(16))
 match1 = db.Column(db.String(512))
 match2 = db.Column(db.String(512))
 created_at = db.Column(db.TIMESTAMP())
 update_at = db.Column(db.TIMESTAMP())

# To return all struct for each tuple
 def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


