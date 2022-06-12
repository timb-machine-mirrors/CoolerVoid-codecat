from application import create_app
from flask import Flask, session, request, abort
from werkzeug import serving
import ssl
import sys
import os

HTTPS_ENABLED = True
VERIFY_USER = True

API_CRT = "cert/client.crt"
API_KEY = "cert/client.key"
API_CA_T = "cert/root_ca.crt"

app = create_app()
app.config.update(
 SESSION_COOKIE_SECURE=True,
 SESSION_COOKIE_HTTPONLY=True,
 SESSION_COOKIE_SAMESITE='Lax',
)

# hardening https://flask.palletsprojects.com/en/1.1.x/security/
@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline';"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# allow list of ip address
@app.before_request
def limit_remote_addr():
 with open("application/allow_list/addr.txt",encoding="utf-8") as fp:
  for line in fp:
   if request.remote_addr == line.strip():
    return
 abort(403)  

if __name__ == "__main__":
#    context = None
#    if HTTPS_ENABLED:
#        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#        if VERIFY_USER:
#            context.verify_mode = ssl.CERT_REQUIRED
#            context.load_verify_locations(API_CA_T)
#        try:
#            context.load_cert_chain(API_CRT, API_KEY)
#        except Exception as e:
#            sys.exit("Error starting flask server. " + "Missing cert or key. Details: {}".format(e))
    app.secret_key = os.environ['CODECAT_APPKEY']
# if you need use your cert change 'adhoc' to context var
    app.run(host='0.0.0.0',port=50093,debug='False',ssl_context='adhoc')
