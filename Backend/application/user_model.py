from . import db
import time
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import inspect

key_secret = "test KEY TeSt asdasda f ef3t4gdf"

class User(db.Model):
 __tablename__ = 'userronin'
 id = db.Column(db.Integer, primary_key=True)
 login = db.Column(db.String(30), unique=True)
 passhash = db.Column(db.String(128))
 mail = db.Column(db.String(128), unique=True)
 last_ip = db.Column(db.String(40))
 owner = db.Column(db.String(12))
 created_at = db.Column(db.TIMESTAMP())
 update_at = db.Column(db.TIMESTAMP())

# To return all struct on tuple
 def toDict(self):
  return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
 def hash_password(self, password):
  self.passhash = pwd_context.encrypt(password)

 def verify_password(self, password):
  return pwd_context.verify(password, self.passhash)

# long expiration for debug purposes
 def generate_auth_token(self, expiration=6000000):
  s = Serializer(key_secret, expires_in=expiration)
  return s.dumps({'id': self.id})

 @staticmethod
 def verify_auth_token(token):
  s = Serializer(key_secret)
  try:
   data = s.loads(token)
  except SignatureExpired:
   return None    # valid token, but expired
  except BadSignature:
   return None    # invalid token
  user = User.query.get(data['id'])
  return user
