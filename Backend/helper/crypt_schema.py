from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import nacl.pwhash
import os

def update_key(input):
 return input+os.environ['CODECAT_SECRET']

def use_argon(input):
 input=update_key(input)
 input=input.encode('ascii')
 password=nacl.pwhash.argon2i.str(input)
 ret = b64encode(password).decode('UTF-8')
 return ret
  

def is_argon_valid(password,test):
 try:
  password=update_key(password)
  password=password.encode('ascii')
  test=b64decode(test)
  nacl.pwhash.verify(test,password) 
  return True
 except nacl.exceptions.CryptoError:
  return False


def custom_random_key_gen():
 input=get_random_bytes(32)
 key=str(b64encode(input).decode('UTF-8'))
 return key


def encrypt_chacha(input):
 key=os.environ['CODECAT_CHACHA'] 
 key=b64decode(key)
 plaintext = input #.encode('ascii')
 cipher = ChaCha20.new(key=key)
 ciphertext = cipher.encrypt(plaintext)
 nonce = b64encode(cipher.nonce).decode('utf-8')
 ct = b64encode(ciphertext).decode('utf-8')
 result=nonce+":"+ct
 return result


def decrypt_chacha(input):
 key=os.environ['CODECAT_CHACHA'] 
 key=b64decode(key)
 keys=input.split(":")
 ct=keys[1]
 nonce=keys[0]
 try:
  nonce = b64decode(nonce)
  ciphertext = b64decode(ct)
  cipher = ChaCha20.new(key=key, nonce=nonce)
  plaintext = cipher.decrypt(ciphertext)
  return plaintext.decode('UTF-8')
 except (ValueError, KeyError):
  print("Incorrect decryption")



